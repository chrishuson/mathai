# Functions to list files and crawl directories for problem set files

import os

import numpy as np
import pandas as pd

from class_organization import Problem, ProblemSet

def map_course_files(course_dir='/Users/chris/GitHub/course-files/Geometry'):
    """ Crawl through unit directories to return dict & df of tex files.

        course_dir - str, path to local directory of files
        returns course files as dict and as dataframe
            {unit: list of file names} (strings)
            "unit", "file_count" (int), "filename"
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
        for filename in course_files[unit]:
            file_list.append((unit, length, filename))
    course_files_df = pd.DataFrame(file_list)
    column_names = ['unit', 'file_count', 'filename']
    course_files_df.columns = column_names

    return course_files, course_files_df


def parse_course_files(course_files_df,
            course_dir='/Users/chris/GitHub/course-files/Geometry'):
    """ Step through worksheets and parse them into problem sets.

        course_files_df - "unit", "file_count" (int), "filename"
        course_dir - str, path to local directory of files
        returns problem_sets_df: 'filename', 'head', 'body', 'problems_list',                                   'problem_count', 'problem_set_ID'
        """
    problem_set_tuples = []
    filenames = (course_dir + '/' + course_files_df.unit + '/'
                + course_files_df.filename)
    for filename in filenames:
        packages, head, body = parse_tex_file(filename)
        problem_set_tuples.append((filename, head, body))
    problem_sets_df = pd.DataFrame(problem_set_tuples)
    problem_sets_df.columns = ['filename', 'head', 'body']
    problem_sets_df['problem_set_ID'] = problem_sets_df.index
        
    try:
        problem_sets_df['problems_list'] = problem_sets_df['body'].apply(parse_body)
    except:
        print('Exception on apply (parse_body). Returning partial problem_sets_df')
        return problem_sets_df
    problem_sets_df['problem_count'] = problem_sets_df['problems_list'].apply(len)
    return problem_sets_df


def parse_problem_sets(problem_sets_df):
    """ Expand problem_sets' problems lists into separate rows of a df.

        problem_sets_df: 'problem_set_ID', 'problems_list'
        returns problems_df: 'problem_set_ID', 'question' - str
        """
    all_questions = np.hstack(problem_sets_df.problems_list)
    all_problem_set_IDs = np.hstack([[ID]*len(problems) for ID, problems in 
                        problem_sets_df[['problem_set_ID', 'problems_list']].values])
    
    problems_df = pd.DataFrame({'problem_set_ID':all_problem_set_IDs, 
                                'question':all_questions})
    return problems_df


def parse_tex_files(file_list=None):
    """ Read a list of worksheet files and returns a ProblemSet dataframe.

        file_list - list, str names of files to be read
        returns dataframe, filename, date, heading, ProblemSet instance
        """
    if file_list is None:
        file_list = []
    

def parse_tex_file(infile):
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
            print('Opened and read file: \n', infile)
            print('length in lines: ', len(lines))
    except FileNotFoundError:
        print('Tried to open non-existent file: ' + infile)
        return None, None, None

    line = lines.pop(0)
    print('1 - packages section. first line: \n', line)
    while lines and r'\begin{document}' not in line:
        packages.append(line)
        line = lines.pop(0)
    print('2 - header section. first line: \n', line)
    while lines and r'\begin{enumerate}' not in line:
        header.append(line)
        line = lines.pop(0)
    print('3 - body section. first line \n', line)
    try:
        line = lines.pop(0)
    except IndexError:
        print('my IndexError: pop from empty list', infile)
    while lines and r'\end{document}' not in line:
        body.append(line)
        line = lines.pop(0)
    print('4 - last line: \n', line)
    return packages, header, body

def parse_body(body_lines):
    """ Parses the body of a tex problem set into separate problems
        
        body - list of text lines
        returns - problems: list of problem strings
            spacing: list of section and formatting text lines
        """
    body = body_lines.copy()
    spacing = []
    nested = False
    problem = []
    problems = []
    
    if type(body) != list:
        print('body needs to be a list, but its type was: ', type(body))
        return []
    try:
        line = body.pop(0)
    except IndexError:
        print('Tried to run parse_body on empty file')
        return []

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
    return problemstextblock #, spacing

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

short_df['fullfilename'] = course_dir + '/' + short_df.unit + '/' + short_df.filename

short_df['text_tuple'] = short_df.fullfilename.apply(parse_tex_file)

short_df[['packages', 'header', 'body']] = pd.DataFrame(short_df.text_tuple.tolist(), index=short_df.index)

short_df[['problems', 'spacing']] = pd.DataFrame(short_df.problem_tuple.tolist(), index=short_df.index)

for unit in course_files:
    print(unit, len(course_files[unit]))

print(set(course_frame['unit']))
print(course_frame[course_frame['unit'].isin(['Misc'])])

course_frame.to_csv('crawler_course_frame.csv') # ,index=False to avoid saving
new = pd.read_csv('crawler_course_frame.csv')

worksheet_path = dbdir + '/' + 'worksheet_files_df.csv' #better os.path.join(list)
worksheet_files_df = pd.read_csv(worksheet_path)
worksheet_files_df.tail(10)

filename = 'problems_df'
problems_df.to_csv(os.path.join(dbdir, filename+'.csv'))
short_problems_df = pd.read_csv(os.path.join(dbdir, 'short_problems_df.csv'))

problem_sets_df = parse_course_files(worksheet_files_df)

To combine problem question text from a dataframe, first make list into string:
    lines = ps_df.agg(lambda x: ''.join(x))
        then join into a long string for printing
    out = lines.str.cat(sep=r'\n') , or also line = 'abc'.join(lines)

pass unit and filename to parse_tex_file:
filenames = os.path.join([course_dir, worksheet_files_df.unit, worksheet_files_df.filename])
    """