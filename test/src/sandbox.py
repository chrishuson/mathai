
#import sys
import os
#import csv
#import pickle
#from collections import namedtuple

from class_organization import Problem, ProblemSet #, DifferentiatedProblemSet, Assessment, \
#                                Course, Student, assign_problem_set
from main import lookup_new_problem_id

HOME = os.environ["HOME"]
#dbdir = HOME + "/GitHub/mathai/db/"
#outdir = HOME + "/GitHub/mathai/out/"
#indir = HOME + "/GitHub/mathai/in/"
indir = HOME + "/GitHub/mathai/test/in/"


def saveproblem(problem, topic="Writing Linear Equations", \
                difficulty=5, problemID=0):
    '''problem: list of text lines
        topic, difficulty: branches of problem dictionary
        problemID: assigned if not given as argument
        
        returns problem in global_problem_dict format
        '''
    if problemID == 0:
        problemID = lookup_new_problem_id(topic, difficulty)
    problemdict = {topic: {difficulty:{0:'null problem instance'}}}
    problemdict[topic][difficulty].update({problemID: Problem(topic, {"question": problem})})
    problemdict[topic][difficulty].pop(0)
    return problemdict
    
def trim_item_prefix(problem):
    '''notes for deleting the initial 'item' text from a problem'''
    firstline = problem[0]
    if r'\item' in firstline:
        for index in range(len(firstline) - 6):
            if firstline[index:index+5] == r'\item':
                problem[0] = firstline[index+6 :]
    return problem

def assign_subsection_to_topic(line):
    '''notes on formatting subsection heading as topic for problems
    '''
    topic = None
    if r"\subsection*" in line:
                for index in range(len(line) - 13):
                    if line[index:index+12] == r"\subsection*":
                        topic = line[index+13:-2]
    return topic


def parsetexfile(infile):
    '''takes full directory name of file
    returns tuple of three lists of text lines
    the top packages section, header lines, and body text
    '''
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
    '''body: list of text lines
    
    returns problems: list of problems, each a list of text lines
    spacing: list of section and formatting text lines
    '''
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
            nested = False
            problem.append(line)
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
    return problems, spacing

def runtest():
    infile = indir + 'parse_test1' + ".tex"
    print('running test on: ' + infile)
    packages, header, body = parsetexfile(infile)
    print('lengths should be 11, 3, 37')
    print(len(packages), len(header), len(body))
    savebody = body[:]
    problems, spacing = parsebody(body)
    print('length of problems should be 8: ')
    print(len(problems))
    return problems, spacing, packages, header, savebody
    
testtitles = []
testtitles.append(('parse_test1', '07/11/2019', 'First file to parse'))
testtitles.append(('parse_test2', '07/12/2019', '2nd file to parse'))
testtitles.append('Title Error case: title is a single string')
testtitles.append(("13-5HW-triangles", "ids in margin", \
             "Parsed from file: in/13-5HW-triangles.tex")) #non-existent file

for title in testtitles:
    print('\n', 'running test on: ', title)
    if type(title) != tuple:
        print('title must be tuple of filename, date, heading note. it was:')
        print(title)
    else:
        infile = indir + title[0] + ".tex"

        packages, header, body = parsetexfile(infile)
        if packages and header and body:
            print(len(packages), len(header), len(body))
        else:
            print('parsetexfile returned empty file(s)')

        problems, spacing = parsebody(body)
        if problems and spacing:
            print(len(problems))
            print(problems[-1])
        else:
            print('parsebody returned empty file(s)')