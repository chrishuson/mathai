
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

