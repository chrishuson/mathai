
#import sys
import os
#import csv
#import pickle
#from collections import namedtuple

from class_organization import Problem #ProblemSet, DifferentiatedProblemSet, Assessment, \
#                                Problem, Course, Student, assign_problem_set
from main import lookup_new_problem_id

HOME = os.environ["HOME"]
#dbdir = HOME + "/GitHub/mathai/db/"
#outdir = HOME + "/GitHub/mathai/out/"
indir = HOME + "/GitHub/mathai/in/"


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
    '''notes for deleting the initial '\item' text from a problem'''
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
    if "\subsection*" in line:
                for index in range(len(line) - 13):
                    if line[index:index+12] == "\subsection*":
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
    
    with open(infile, "r") as texfile:
        lines = texfile.readlines()
        print(len(lines))
        
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
    
    line = body.pop(0)
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
    
#title = ("1214IB1_Test-exponentials", "ids in margin", \
#             "Parsed from file: in/1214IB1_Test-exponentials.tex")
title = ("13-5HW-triangles", "ids in margin", \
             "Parsed from file: in/13-5HW-triangles.tex")
infile = indir + title[0] + ".tex"

packages, header, body = parsetexfile(infile)
print(len(packages), len(header), len(body))

problems, spacing = parsebody(body)
print(len(problems))
print(problems[-1])