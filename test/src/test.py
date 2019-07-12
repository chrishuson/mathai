
#import sys
import os
#import csv
#import pickle
#from collections import namedtuple

#from class_organization import Problem, ProblemSet #, DifferentiatedProblemSet, Assessment, \
#                                Course, Student, assign_problem_set
#from main import lookup_new_problem_id
#import main

HOME = os.environ["HOME"]
#dbdir = HOME + "/GitHub/mathai/db/"
#outdir = HOME + "/GitHub/mathai/out/"
#indir = HOME + "/GitHub/mathai/in/"
indir = HOME + "/GitHub/mathai/test/in/"


def saveproblem(problem, topic="Writing Linear Equations", \
                difficulty=5, problemID=0):
    ''' 
    
        problem: list of text lines
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
    
def assign_subsection_to_topic(line):
    '''notes on formatting subsection heading as topic for problems
    '''
    topic = None
    if r"\subsection*" in line:
                for index in range(len(line) - 13):
                    if line[index:index+12] == r"\subsection*":
                        topic = line[index+13:-2]
    return topic


def test_parse(testtitles = []):
    """ Uploads tex file, parses it into sections then problems

        testtitles - list of title tuples, each containing (filename, date, worksheet title)
        returns 5-tuple of intermediate results: problems, spacing, packages, header, body
        """
    if testtitles == []:
        print('loading default filenames')
        testtitles.append(('parse_test1', '07/11/2019', 'First file to parse'))
        testtitles.append(('parse_test2', '07/12/2019', '2nd file to parse'))
        testtitles.append(('parse_test3', '05/12/2019', '11-2HW_slope-applications'))
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
                if title[0] == 'parse_test1':
                    print('lengths should be 11, 3, 37')
                print(len(packages), len(header), len(body))
                savebody = body[:]
            else:
                print('parsetexfile returned empty file(s)')

            problems, spacing = parsebody(body)
            if problems and spacing:
                if title[0] == 'parse_test1':
                    print('length of problems should be 8: ')
                elif title[0] == 'parse_test3':
                    print('length of problems should be 10: ')
                print(len(problems))
                print(problems[-1])
            else:
                print('parsebody returned empty file(s)')
    return problems, spacing, packages, header, savebody