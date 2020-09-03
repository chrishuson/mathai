#File of problem set data structures and editing, printing functions
# $ python main.py    (from /Users/chris/GitHub/mathai/src directory)


import sys
import os
import csv
import ast

import numpy as np
import pandas as pd

TESTFLAG = False
if TESTFLAG:
    os.chdir('/Users/chris/GitHub/mathai/test/src')
    #import unit_tests

HOME = os.environ["HOME"]
db_dir = HOME + "/GitHub/mathai/db/"
out_dir = HOME + "/GitHub/mathai/out/"
in_dir = HOME + "/GitHub/mathai/in/"
course_dir = HOME + "/GitHub/course-files/Geometry"

if TESTFLAG:
    db_dir = HOME + "/GitHub/mathai/test/db/"
    out_dir = HOME + "/GitHub/mathai/test/out/"
    in_dir = HOME + "/GitHub/mathai/test/in/"


def save_csv(filenames=None, db_dir=db_dir): #convert to **arg format
    """ Save persistent record in db directory of dataframes

        filenames - list of tuples, dataframe and csv filenames to save
         ("problem_sets_df", "standards_text_jmap", "standards_tree_jmap")
        """
    if filenames is None:
        filenames = [(problem_sets_df, 'problem_sets_df'), 
                      (problems_df, 'problems_df')]
    try:
        for df, filename in filenames:
            path_plus_filename = os.path.join(db_dir, filename+'.csv')
            df.to_csv(path_plus_filename)
    except:
        print('Something wrong. arg should be list of tuples.')
    return None


def load_csv(filenames=None, db_dir=db_dir): #TODO eliminate function
    """ Return records of dataframes from db directory csv files

        filenames - list of csv filenames to load
        return - list of dataframes [problem_sets_df, problems_df]
        """
    if filenames is None:
        filenames = ['problem_sets_df', 'problems_df']
    result_dfs = []
    for filename in filenames:
        path_plus_filename = os.path.join(db_dir, filename+'.csv')
        try:
            df = pd.read_csv(path_plus_filename)
            result_dfs.append(df)
        except:
            print('Something wrong. arg should be list of filenames without extension.')
    return result_dfs

def print_problem_set_df(problem_sets_df, problems_df, out_dir=out_dir):
    """ Save tex file for each problem set row's problem list.

        problem_sets_df - 'problem_IDs', list; 'unit', str; 'out_filename', str
                        'title', 3-tuple str's
        problems_df - index problem_ID, 'question', str
        out_dir - str, path to save problem set files, under unit directories
        returns out_files_df - 'filename', 'unit'
        """
    out_files = []
    for problem_set_ID, problem_set_row in problem_sets_df.iterrows():
        filename = 'Problem_set_ID_' + str(problem_set_ID)
        #path_plus_filename = os.path.join(out_dir, 'unit_tmp', filename)
        title = ('Problem set subheading', 
                'Problem set ID ' + str(problem_set_ID), 'tmp Geometry')
        ps_problems_df = problems_df.loc[problem_set_row.problem_IDs]
        print_problems_df(ps_problems_df, filename, title)
        out_files.append((filename + '.tex', 'unit_xyz'))
    return pd.DataFrame(out_files, columns=['filename', 'unit']) #index should match problem_set_ID

def print_problems_df(problems_df, filename='tmp', title=None, meta=False, numflag=True):
    """ Creates a worksheet LaTeX file composed of problem questions.

        problems_df - 'question' str, 'problem_set_ID'
        filename - str, name of tex file created in out directory
        title - 3-tuple, str (worksheet sub heading, date, margin head)
        meta - bool, include Problem meta data (ID, Topic, difficulty, etc.)
        numflag - bool, include "{enumerate}" environment, "item" Problem prefix
        output file is filename.tex in the out_dir directory
        """
    out_file = out_dir + filename + ".tex"
    head = make_tex_head(title)
    with open(out_file, "w") as newfile:
        for line in head:
            newfile.write(line)
        if numflag:
            newfile.write(r'\begin{enumerate}' + '\n')
        
        prefix = '\n' + r'\item '
        problem_tex = problems_df.question.str.cat(sep=prefix)
        problem_tex = prefix + problem_tex
        newfile.write(problem_tex)

        if numflag:
            newfile.write('\n' + r'\end{enumerate}'+'\n')
        newfile.write(r'\end{document}' + '\n')

def make_tex_head(title=None):
    """ Reads the head.tex file to make the first lines of a tex file.

        title - 3-tuple, str (worksheet sub heading, date, margin head)
        returns - str, tex header section of printable problem set file
        """
    try:
        with open(db_dir + 'head.tex', 'r') as f:
            head = f.read()
    except FileNotFoundError:
            print('Found no file head.tex in directory', db_dir)
            head = ''
    if title is None:
        head += (r'\fancyhead[L]{BECA / Dr. Huson}' + '\n'*2 
                + r'\begin{document}' + '\n'*2)
    else:
        head += (r'\fancyhead[L]{BECA / Dr. Huson / '
                + title[2] + r'\\* ' + title[1] + r'}')
        head += '\n'*2 + r'\begin{document}' + '\n'*2
        head += r'\subsubsection*{' + title[0] + '}\n'
    return head


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
    """ Step through worksheets and parse them into problem sets df.

        course_files_df - "unit", "file_count" (int), "filename"
        course_dir - str, path to local directory of files
        returns problem_sets_df: 'filename', 'head', 'body', 'problems_list',
                                    'problem_count', 'problem_set_ID'
        """
    problem_set_tuples = []
    filenames = (course_dir + '/' + course_files_df.unit + '/'
                + course_files_df.filename)
    for filename in filenames:
        head, body = parse_tex_file(filename)
        problem_set_tuples.append((filename, head, body)) # TODO make filename w/o path by using course_files_df
    problem_sets_df = pd.DataFrame(problem_set_tuples)
    problem_sets_df.columns = ['filename', 'head', 'body']
    problem_sets_df.index.name = 'problem_set_ID'
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
    all_problem_set_IDs = np.hstack([[ID]*problem_count for ID, problem_count in 
                                problem_sets_df.problem_count.iteritems()])
                        #problem_sets_df[['problem_set_ID', 'problems_list']]#.values]) #TODO set as index
    
    problems_df = pd.DataFrame({'problem_set_ID':all_problem_set_IDs, 
                                'question':all_questions})
    problems_df.index.name = 'problem_ID'
    return problems_df


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
            #print('Opened and read file: \n', infile)
            #print('length in lines: ', len(lines))
    except FileNotFoundError:
        print('Tried to open non-existent file: ' + infile)
        return None, None, None

    line = lines.pop(0)
    #print('1 - packages section. first line: \n', line)
    while lines and r'\begin{document}' not in line:
        packages.append(line)
        line = lines.pop(0)
    #print('2 - header section. first line: \n', line)
    while lines and r'\begin{enumerate}' not in line:
        header.append(line)
        line = lines.pop(0)
    #print('3 - body section. first line \n', line)
    try:
        line = lines.pop(0)
    except IndexError:
        print('my IndexError: pop from empty list', infile)
    while lines and r'\end{document}' not in line:
        body.append(line)
        line = lines.pop(0)
    #print('4 - last line: \n', line)
    return header, body

def parse_body(body_lines):
    """ Parses the body of a tex problem set into separate problems
        
        body - list of text lines
        returns - problems: list of problem strings
            spacing: list of section and formatting text lines

        ISSUES: newlines new pages, bracketed items or begin multicols before item (eg 9-1DN...)
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
        elif r'\subsubsection' in line:
            while r'\item' not in line and body:
                line = body.pop(0)
            problem = []
            problem.append(line)
        elif r'\newpage' in line: #newlines are saved as problems
            spacing.append(line)
            problems.append(problem)
            problem = []
            problem.append(line)
            problems.append(problem)
            problem = []
        elif r'\item' in line and r'\begin{enumerate}' in line and not nested:
            nested = True
            problems.append(problem)
            problem = []
            problem.append(line)
        elif r'\item' in line and not nested:
            problems.append(problem)
            problem = []
            problem.append(line)
        elif r'\begin{enumerate}' in line:
            nested = True
            problem.append(line)
        elif r'\begin{itemize}' in line:
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
        elif r'\end{itemize}' in line:
            if nested:
                nested = False
                problem.append(line)
            else:
                spacing.append(line)
                problems.append(problem)
                problem = []
        else:
            problem.append(line)
        if body:
            line = body.pop(0)
    problems.append(problem)

    newline = ['\n']
    while True:
        try: 
            problems.remove(newline)
        except:
            break
    newline2 = ['\n', '\n']
    while True:
        try: 
            problems.remove(newline2)
        except:
            break
    newline3 = [r' \n']
    while True:
        try: 
            problems.remove(newline3)
        except:
            break
    newline4 = [r'  \n']
    while True:
        try: 
            problems.remove(newline4)
        except:
            break
    newline5 = [r'    \n']
    while True:
        try: 
            problems.remove(newline5)
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

def add_problem_IDs_to_set(problem_sets_df): #TODO pass in problems_df as argument
    """ Add list of problem_IDs to each problem_set.

        problem_sets_df - index 'problem_set_ID'
        problems_df - index 'problem_ID
        returns problem_sets_df with column 'problem_IDs', list
        """
    p_sets_copy = problem_sets_df.copy()
    problem_IDs = []
    for problem_set_ID in p_sets_copy.index:
        problem_IDs.append(
            [p_ID for p_ID in problems_df[problems_df.problem_set_ID == problem_set_ID].index])
    p_sets_copy['problem_IDs'] = problem_IDs
    return p_sets_copy


worksheet_files_df, standards_df = load_csv(['worksheet_files_df', 'standards_df'])

filename = 'problem_sets_df'
path_plus_filename = os.path.join(db_dir, filename+'.csv')
problem_sets_df = pd.read_csv(path_plus_filename, index_col='problem_set_ID')
problem_sets_df['head'] = problem_sets_df['head'].apply(ast.literal_eval)
problem_sets_df['body'] = problem_sets_df['body'].apply(ast.literal_eval)
problem_sets_df['problems_list'] = problem_sets_df['problems_list'].apply(ast.literal_eval)
problem_sets_df['problem_IDs'] = problem_sets_df['problem_IDs'].apply(ast.literal_eval)

filename = 'problems_df'
path_plus_filename = os.path.join(db_dir, filename+'.csv')
problems_df = pd.read_csv(path_plus_filename, index_col='problem_ID')

filename = 'standards_desc_df'
path_plus_filename = os.path.join(db_dir, filename+'.csv')
standards_desc_df = pd.read_csv(path_plus_filename, index_col='ccss_ID')
#standards_desc_df.to_csv(path_plus_filename)

"""
filename = 'standards_df'
path_plus_filename = os.path.join(db_dir, filename+'.csv')
standards_df.to_csv(path_plus_filename, index=False)
        worksheets_df also doesn't have an index column """

#problem_sets_df = parse_course_files(worksheet_files_df)
#print_problems_df(problems_df[problems_df['problem_set_ID']==5], 'tmp2')

print('Loaded dataframes: ')
print('worksheet_files_df:\n', 
        'index name: ', worksheet_files_df.index.name,
        '\ncolumns: ', worksheet_files_df.columns, 
        '\n149 rows: ', len(worksheet_files_df), '\n')
print('problem_sets_df:\n', 
        'index name: ', problem_sets_df.index.name,
        '\ncolumns: ', problem_sets_df.columns, 
        '\n149 rows: ', len(problem_sets_df), '\n')
print('problems_df:\n', 
        'index name: ', problems_df.index.name,
        '\ncolumns: ', problems_df.columns, 
        '\n1855 rows: ', len(problems_df), '\n')
print('standards_df:\n', 
        'index name: ', standards_df.index.name,
        '\ncolumns: ', standards_df.columns, 
        '\n314 rows: ', len(standards_df), '\n')
print('standards_desc_df:\n', 
        'index name: ', standards_desc_df.index.name,
        '\ncolumns: ', standards_desc_df.columns, 
        '\n131 rows: ', len(standards_desc_df), '\n')

""" df select for string in body, i.e. a list of strings
    def check_for_setcounter(body_list):
        return any('setcounter' in line for line in body_list)

    setcounter_df = problem_sets_df[problem_sets_df.body.apply(check_for_setcounter)]"""