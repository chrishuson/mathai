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
course_dir = HOME + "/GitHub/course-files/Geom2021/"

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

def build_pset_df_pdf(pset_df, problem_df, course_dir='/Users/chris/GitHub/course-files/Geom2021/'): # consider .to_pdf, tex
    #os.chdir('/Users/chris/GitHub/course-files/Geom2021/02-Midpoint+distance') #needs to move to proper unit directory
    for pset in pset_df.itertuples():
        unit_dir = course_dir + pset.unit
        path_plus_filename = unit_dir + '/' + pset.filename
        if 'path_plus_filename' in pset_df.columns:
            path_plus_filename = pset.path_plus_filename
            unit_dir = path_plus_filename.rsplit('/', 1)[0]
        pdf_dir = unit_dir + '/pdf'
        try:
            os.chdir(unit_dir)
        except: 
            print('could not change directory to ', unit_dir)
        os.system('pdflatex -output-directory=' + pdf_dir + ' ' + path_plus_filename) #TODO check for pdf subdirectory


def build_pset_df_tex(pset_df, problem_df, course_dir='/Users/chris/GitHub/course-files/Geom2021/'):
    """ Save tex file for each problem set row's problem list.

        pset_df - index 'pset_ID'; 'problem_IDs', list; 'unit', str; 'file', str
            optionally full path to filename saved
        problem_df - index 'problem_ID'; 'question', str
        returns built tex files df - index 'pset_ID', 'filename', 'unit'
        """
    out_files = []
    for pset in pset_df.itertuples():
        if 'path_plus_filename' in pset_df.columns:
            path_plus_filename = pset.path_plus_filename
        else: path_plus_filename = course_dir + pset.unit + '/' + pset.filename

        title = (pset.filename.replace('_', '-')[:-4], #underbars in text cause pdflatex error
                'pset ID: ' + str(pset.Index),
                'Geometry ' + pset.unit.replace('_', '-'))
        build_problem_df_tex(problem_df.loc[pset.problem_IDs],
                            pset.filename, title, path_plus_filename)
        out_files.append((pset.Index, pset.filename, pset.unit, path_plus_filename))
    return pd.DataFrame(out_files, columns=['pset_ID', 'filename', 'unit', 'path_plus_filename']).set_index('pset_ID')

def build_problem_df_tex(problem_df, filename='tmp.tex', title=None, path_plus_filename=None, meta=False):
    """ Creates a worksheet LaTeX file composed of problem questions.

        problem_df - 'question' str, 'problem_set_ID'
        filename - str, name of tex file created in out directory (with '.tex' extension)
        title - 3-tuple, str (worksheet sub heading, date, margin header)
        meta - bool, include Problem meta data (ID, Topic, difficulty, etc.)
        tex doc is saved as filename.tex in the out_dir, or full path and filename if given
        """
    if path_plus_filename==None: path_plus_filename = out_dir + filename
    try:
        with open(db_dir + 'header.tex', 'r') as f:
            latex_body = f.read()
    except FileNotFoundError:
            print('Found no file header.tex in directory', db_dir)
            latex_body = r'\documentclass[12pt, twoside]{article}' + '\n'
    if title is None:
        latex_body += (r'\fancyhead[LO]{BECA / Dr. Huson}' + '\n'*2 
                + r'\begin{document}' + '\n'*2)
    else:
        latex_body += (r'\fancyhead[LO]{BECA / Dr. Huson / '
                + title[2].replace('_', '-') + r'\\* '  #underbars in text cause pdflatex error
                + title[1].replace('_', '-') + r'}')
        latex_body += '\n'*2 + r'\begin{document}' + '\n'*2
        latex_body += (r'\subsubsection*{' 
                + title[0].replace('_', '-') + '}\n')
    latex_body += r'\begin{enumerate}' + '\n'

    for q in problem_df.question:
        if r'\newpage' in q or 'subsection' in q:
            latex_body += q
        else:
            latex_body += r'\item ' + q
    latex_body += (r'\end{enumerate}' + '\n'
                + r'\end{document}')
    #pdf = latex.build_pdf(latex_body)
    with open(path_plus_filename, "w") as f:
        f.write(latex_body)

def print_problem_set_df(problem_sets_df, problems_df, out_dir=out_dir): #replaced by build_pset_df_tex
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

def print_problems_df(problems_df, filename='tmp', title=None, meta=False, numflag=True):  #replaced by build_problem_df_tex
    """ Creates a worksheet LaTeX file composed of problem questions.

        problems_df - 'question' str, 'problem_set_ID'
        filename - str, name of tex file created in out directory
        title - 3-tuple, str (worksheet sub heading, date, margin header)
        meta - bool, include Problem meta data (ID, Topic, difficulty, etc.)
        numflag - bool, include "{enumerate}" environment, "item" Problem prefix
        output file is filename.tex in the out_dir directory
        """
    out_file = out_dir + filename + ".tex"
    header = make_tex_header(title)
    with open(out_file, "w") as newfile:
        for line in header:
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

def make_tex_header(title=None):  #replaced by build_problem_df_tex
    """ Reads the header.tex file to make the first lines of a tex file.

        title - 3-tuple, str (worksheet sub heading, date, margin header)
        returns - str, tex header section of printable problem set file
        """
    try:
        with open(db_dir + 'header.tex', 'r') as f:
            header = f.read()
    except FileNotFoundError:
            print('Found no file header.tex in directory', db_dir)
            header = ''
    if title is None:
        header += (r'\fancyhead[LO]{BECA / Dr. Huson}' + '\n'*2 
                + r'\begin{document}' + '\n'*2)
    else:
        header += (r'\fancyhead[LO]{BECA / Dr. Huson / '
                + title[2] + r'\\* ' + title[1] + r'}')
        header += '\n'*2 + r'\begin{document}' + '\n'*2
        header += r'\subsubsection*{' + title[0] + '}\n'
    return header


def map_course_files(course_dir='/Users/chris/GitHub/course-files/Geom'):
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


def parse_course_files(course_file_df,
            course_dir='/Users/chris/GitHub/course-files/Geom'):
    """ Step through worksheets and parse them into problem set df.

        course_file_df - "unit", "file_count" (int), "filename"
        course_dir - str, path to local directory of files
        returns pset_df: 'unit', 'file', 'problem_count', 'problems_list', 'problem_kind', 
                        'head', 'body',  'path', 'filename'
        """
    #pset_tuples = []
    #filenames = (course_dir + '/' + course_file_df.unit + '/'
    #            + course_file_df.filename)
    #for filename in filenames:
    #    head, body = parse_tex_file(filename)
    #    pset_tuples.append((filename, head, body)) # TODO make filename w/o path by using course_file_df
    
    pset_df = course_file_df[['unit', 'filename']].copy()
    pset_df.index.name = 'problem_set_ID'
    
    pset_df[['head', 'body']] = pset_df.apply(lambda x: parse_tex_file(course_dir + '/' + x.unit + '/' + x.filename), axis=1, result_type='expand')

    #pset_df = pd.DataFrame(pset_tuples)
    #pset_df.columns = ['filename', 'head', 'body']
    #pset_df.index.name = 'problem_set_ID'
    try:
        pset_df[['problems_list', 'problem_kind']] = pset_df.apply(lambda x: parse_body(x.body), axis=1, result_type='expand')
    except:
        print('Exception on apply (parse_body). Returning partial pset_df')
        return pset_df
    pset_df['problem_count'] = pset_df['problems_list'].apply(len)
    
    #return pset_df, None

    problem_df = parse_problem_sets(pset_df)

    problem_IDs = []
    for problem_set_ID in pset_df.index:
        problem_IDs.append(
            [p_ID for p_ID in problem_df[problem_df.problem_set_ID == problem_set_ID].index])
    pset_df['problem_IDs'] = problem_IDs
    
    new_cols = ['unit', 'filename', 'problem_count', 'problem_IDs', 'problems_list', 'problem_kind', 'head', 'body']
    pset_df = pset_df.reindex(columns=new_cols)
    
    return pset_df, problem_df


def parse_problem_sets(pset_df):
    """ Expand problem_sets' problems lists into separate rows of a problem df

        pset_df: index 'problem_set_ID'; 'problems_list', 'problem_kind'
        returns problem_df: 'problem_set_ID', 'question' (str), 'kind', 'filename', 
                            'q_len' (length of question text)
        """
    all_questions = np.hstack(pset_df.problems_list)
    all_kinds = np.hstack(pset_df.problem_kind)
    all_problem_set_IDs = np.hstack([[ID]*problem_count for ID, problem_count in 
                                pset_df.problem_count.iteritems()])
    
    #print('all_kinds: ', len(all_kinds))
    #print('all_problem_set_IDs: ', len(all_problem_set_IDs))
    #print('all_questions: ', len(all_questions))
    #print('all_questions: ', all_questions)
    #return None

    problem_df = pd.DataFrame({'problem_set_ID':all_problem_set_IDs, 
                                'question':all_questions, 'kind':all_kinds}) # bug mismatched lengths
    problem_df.index.name = 'problem_ID'

    problem_df['filename'] = problem_df.problem_set_ID.apply(lambda x: pset_df.loc[x, 'filename'])
    problem_df['q_len'] = problem_df.question.str.len()

    return problem_df


def parse_tex_file(full_filename):
    """ divide tex file into three sections
    
        full_filename - str, full directory name of file
        returns tuple of two lists of text lines:
            header lines, and body text
        """
    packages = []
    header = []
    body = []
    
    try:
        with open(full_filename, "r") as texfile:
            lines = texfile.readlines()
    except FileNotFoundError:
        print('Tried to open non-existent file: ' + full_filename)
        return None, None

    line = lines.pop(0)
    while lines and r'\begin{document}' not in line:
        packages.append(line)
        line = lines.pop(0)
    while lines and r'\begin{enumerate}' not in line:
        header.append(line)
        line = lines.pop(0)

    try:
        line = lines.pop(0)
    except IndexError:
        print('my IndexError: pop from empty list', full_filename)
    while lines and r'\end{document}' not in line:
        body.append(line)
        line = lines.pop(0)

    return header, body

def parse_body(body_lines):
    """ Parses the body of a tex problem set into separate problems
        
        body_lines - list of tex lines in problem set
        returns - problems: list of problem and format strings
            kind, list: 'question', 'section', 'newpage', 'multicols'

        ISSUES: newlines new pages, bracketed items or begin multicols before item (eg 9-1DN...)
        """
    body = body_lines.copy()
    enum_ended = False
    nested = 0
    question = False
    multicols = False
    kind = []
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
        if r'\subsection' in line or r'\subsubsection' in line:
            if problem:
                problems.append(problem)
            #print('section start: ', line)
            kind.append('section')
            question = False
            problem = [line]
        elif r'\newpage' in line: 
            if problem:
                problems.append(problem)
            #print('newpage start/end: ', line)
            kind.append('newpage')
            question = False
            problem = [line]
        elif r'{multicols}' in line and not question:
            if problem:
                problems.append(problem)
            #print('multicols "start": ', line)
            kind.append('multicols')
            question = False
            multicols = True
            problem = [line]
        elif r'{multicols}' in line and question and multicols:
            if problem:
                problems.append(problem)
            #print('multicols "start": ', line)
            kind.append('multicols')
            question = False
            multicols = False
            problem = [line]
        elif r'\item' in line and r'\begin{enumerate}' in line and not nested: #missing check for begin-itemize
            if problem:
                problems.append(problem)
            #print('question(+enum) start: ', line)
            kind.append('question')
            nested = 1
            question = True
            problem = [line]
        elif r'\item' in line and not nested:
            if problem:
                problems.append(problem)
            #print('question start: ', line)
            kind.append('question')
            question = True
            problem = [line]
        elif r'\begin{enumerate}' in line:
            #print('continue. enum start: ', line)
            if enum_ended:
                enum_ended = False
                problems.append(problem)
                problem = []
            else:
                #if nested:
                    #print('Warning: Double nested. Not parsed properly.', '\n', problem)
                nested += 1
                problem.append(line)
        elif r'\begin{itemize}' in line:
            #print('continue. itemize start: ', line)
            if enum_ended:
                enum_ended = False
                problems.append(problem)
                problem = []
            else:
                #if nested:
                    #print('Warning: double nested (itemize). Not parsed properly.', '\n', problem)
                nested  += 1
                problem.append(line)
        elif r'\end{enumerate}' in line:
            if nested:
                #print('continue. enum end: ', line)
                nested -= 1
                problem.append(line)
            else:
                #print('end of enum / doc: ', line)
                problems.append(problem)
                problem = []
                enum_ended = True
        elif r'\end{itemize}' in line:
            if nested:
                #print('continue. itemize end: ', line)
                nested  -= 1
                problem.append(line)
            else:
                #print('end of itemize / doc: ', line)
                problems.append(problem)
                problem = []
                enum_ended = True
        else:
            #print('continue: ', line)
            problem.append(line)
        if body:
            line = body.pop(0)
    if problem:
        problems.append(problem)
        
    newline = ['\n']
    while True:
        try: 
            problems.remove(newline)
        except:
            break
    newline2 = [' \n']
    while True:
        try: 
            problems.remove(newline2)
        except:
            break
    newline3 = ['\n', '\n']
    while True:
        try: 
            problems.remove(newline3)
        except:
            break
    trimmedproblems = [trim_item_prefix(problem) for problem in problems]
    problemstextblock = [''.join(problem) for problem in trimmedproblems]
    return problemstextblock, kind

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

def add_problem_IDs_to_set(problem_sets_df): # Legacy, no longer used
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

print('ran main')

"""
worksheet_files_df, standards_df = load_csv(['worksheet_files_df', 'standards_df'])

filename = 'problem_sets_df'
path_plus_filename = os.path.join(db_dir, filename+'.csv')
problem_sets_df = pd.read_csv(path_plus_filename, index_col='problem_set_ID')
problem_sets_df['header'] = problem_sets_df['header'].apply(ast.literal_eval)
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

filename = 'standards_df'
path_plus_filename = os.path.join(db_dir, filename+'.csv')
standards_df.to_csv(path_plus_filename, index=False)
        worksheets_df also doesn't have an index column """

#problem_sets_df = parse_course_files(worksheet_files_df)
#print_problems_df(problems_df[problems_df['problem_set_ID']==5], 'tmp2')

"""
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

    df select for string in body, i.e. a list of strings
    def check_for_setcounter(body_list):
        return any('setcounter' in line for line in body_list)

    setcounter_df = problem_sets_df[problem_sets_df.body.apply(check_for_setcounter)]"""