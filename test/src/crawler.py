# Functions to list files and crawl directories for problem set files

import os

import numpy as np
import pandas as pd

from class_organization import Problem, ProblemSet

def map_course_files(course_dir='/Users/chris/GitHub/course-files/Geometry'):
    """ Crawls through unit directories to return dict of tex files

        course_dir - str, path to local directory of files
        returns course files as dict and as dataframe
            {unit: list of file names} (strings)
            "unit", "worksheet count" (int), "worksheet file name"
        """
    #use scandir instead of listdir
    unit_directories = []
    with os.scandir(course_dir) as d:
        for unit in d:
            if not unit.name.startswith('.') and unit.is_dir():
                unit_directories.append(unit.name)
    unit_directories.sort()
    course_files = {}
    for unit in unit_directories:
        unit_tex_files = []
        with os.scandir(course_dir + r'/' + unit) as d:
            for entry in d:
                if entry.name.endswith('.tex'):
                    unit_tex_files.append(entry.name)
        unit_tex_files.sort()
        course_files[unit] = unit_tex_files
    
    file_list = []
    for unit in course_files:
        length = len(course_files[unit])
        for worksheet in course_files[unit]:
            file_list.append((unit, length, worksheet))
    course_files_df = pd.DataFrame(file_list)
    column_names = ['unit', 'worksheet_count', 'worksheet_file_name']
    course_files_df.columns = column_names

    return course_files, course_files_df


def parse_course_files(course_files_df,
            course_dir='/Users/chris/GitHub/course-files/Geometry'):
    """ Steps through worksheets and parses them into problem sets and problems.

        course_dir - str, path to local directory of files
        course_files_df - "unit", "worksheet count" (int), "worksheet file name"
        returns 
            problem_sets_df: "worksheet file name", ProblemSet instance
            problems_df: "worksheet file name", Problem instance
        """
    problem_set_tuples = []
    problem_tuples = []
    for file_index in range(5):
        filename = (course_dir + r'/' + course_files_df['unit'][file_index] 
            + r'/' + course_files_df['worksheet_file_name'][file_index])
        packages, header, body = parsetexfile(filename)
        problemstextblock, spacing = parsebody(body)
        problems = []
        for problem_text in problemstextblock:
            problems.append(Problem(texts={'question':problem_text}))
        problem_tuples.extend([(course_files_df['worksheet_file_name'][file_index], 
                problem) for problem in problems])
        problem_set_tuples.append((course_files_df['worksheet_file_name'][file_index], 
                ProblemSet(problems)))
    problems_df = pd.DataFrame(problem_tuples)
    problems_df.columns = ['worksheet file name', 'problem instance']
    problem_sets_df = pd.DataFrame(problem_set_tuples)
    problem_sets_df.columns = ['worksheet file name', 'problem set instance']
    return problem_sets_df, problems_df



def parse_tex_files(file_list=None):
    """ Reads a list of worksheet files and returns a ProblemSet dataframe

        file_list - list, str names of files to be read
        returns dataframe, filename, date, heading, ProblemSet instance
        """
    if file_list is None:
        file_list = []
    

def parsetexfile(infile):
    """ divide tex file into three sections
    
        infile - str, full directory name of file
        returns tuple of three lists of text lines:
        the top packages section, header lines, and body text
        """
    packages = []
    header = []
    body = []
    
    try:
        with open(infile, "r") as texfile:
            lines = texfile.readlines()
            print(len(lines))
    except FileNotFoundError:
        print('Tried to open non-existent file: ' + infile)
        return None, None, None

    line = lines.pop(0)
    print('1', line)
    while lines and r'\begin{document}' not in line:
        packages.append(line)
        line = lines.pop(0)
    print('2', line)
    while lines and r'\begin{enumerate}' not in line:
        header.append(line)
        line = lines.pop(0)
    print('3', line)
    line = lines.pop(0)
    while lines and r'\end{document}' not in line:
        body.append(line)
        line = lines.pop(0)
    print('4', line)
    print('finished first parse.')
    return packages, header, body

def parsebody(body):
    """ Parses the body of a tex problem set into separate problems
        
        body - list of text lines
        returns - problems: list of problem strings
            spacing: list of section and formatting text lines
        """
    spacing = []
    nested = False
    problem = []
    problems = []
    
    if type(body) != list:
        print('body needs to be a list, but its type was: ', type(body))
        return None, None
    try:
        line = body.pop(0)
    except IndexError:
        print('Tried to run parsebody on empty file')
        return None, None

    while body:
        if r'\subsection' in line:
            spacing.append(line)
            problems.append(problem)
            problem = []
        elif r'\newpage' in line:
            spacing.append(line)
            problems.append(problem)
            problem = []
        elif r'\item' in line and not nested:
            problems.append(problem)
            problem = []
            problem.append(line)
        elif r'\begin{enumerate}' in line:
            nested = True
            problem.append(line)
        elif r'\end{enumerate}' in line:
            if nested:
                nested = False
                problem.append(line)
            else:
                spacing.append(line)
                problems.append(problem)
                problem = []
        else:
            problem.append(line)
        line = body.pop(0)
    problems.append(problem)

    newline = ['\n']
    while True:
        try: 
            problems.remove(newline)
        except:
            break
    empty = []
    while True:
        try: 
            problems.remove(empty)
        except:
            break
    trimmedproblems = [trim_item_prefix(problem) for problem in problems]
    problemstextblock = [''.join(problem) for problem in trimmedproblems]
    return problemstextblock, spacing

def trim_item_prefix(problem):
    """ Deletes the initial 'item' text, and preceding spaces, 
        from a problem"""
    try:
        firstline = problem[0]
    except IndexError:
        print('Attempt to trim "item" from empty problem: IndexError in trim_item_prefix')
        print(problem)
        return problem
    if r'\item' in firstline:
        for index in range(len(firstline) - 6):
            if firstline[index:index+5] == r'\item':
                problem[0] = firstline[index+6 :]
    return problem


"""
for unit in course_files:
    print(unit, len(course_files[unit]))

print(set(course_frame['unit']))
print(course_frame[course_frame['unit'].isin(['Misc'])])

course_frame.to_csv('crawler_course_frame.csv')
new = pd.read_csv('crawler_course_frame.csv')
    """