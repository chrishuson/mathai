# IMPORTS ROSTERS, PROBLEMS, AND SKILLSETS FROM INDIR,
# SETTING UP GLOBAL DICTS OF COURSES, STUDENTS, AND ProblemS

# For Hydrogen:
#%pwd
#%cd src

import sys
import os
import csv
import pickle
from collections import namedtuple

from main import savedbfile, loaddbfile
from class_organization import ProblemSet, Problem, Course, Student, add_student, \
        add_course, add_problem

HOME = os.environ["HOME"]
dbdir = HOME + "/GitHub/mathai/db/"
outdir = HOME + "/GitHub/mathai/out/"
indir = HOME + "/GitHub/mathai/in/"


# IMPORT INITIAL BATCH OF TOPICS AS LIST OF TEXTS
infile = indir + "skillset_topics.csv"
imported_topics = []
with open(infile, "r", encoding='latin-1') as topics_file:
    f = csv.reader(topics_file, delimiter=',', quotechar='"')
    for row in f:
        imported_topics.append(row[0])
# Fix corruption of first character of first imported topics
imported_topics[0] = "Modeling Exponential Functions"

# IMPORT INITIAL ROSTER AND SKILLSETS
infile = indir + "roster+skillset.csv"
imported_roster = []
imported_skillset = {}
with open(infile, "r", encoding='latin-1') as r_file:
    f = csv.reader(r_file, delimiter=',', quotechar='"')
    for row in f:
        student_name = (row[0], row[1])
        imported_roster.append(student_name)
        student_skillset = dict(zip(imported_topics, row[2:]))
        imported_skillset[student_name] = student_skillset

# IMPORT PROBLEMS AND SET UP FOR DEC 14 PROBLEM SET (TO DO)
problem_data_dict = {} # temporary to make code run

#GLOBAL CREATION OF STUDENTS DICTIONARY {STUDENT NAME TUPLE: STUDENT INSTANCE}
global_students_dict = {} # First time only

student_data_list = imported_roster

# Input is list of tuples, (last, first)
for student_name in student_data_list:
    print(student_name)

student_data_list[0]
alesha = Student(student_data_list[0])

#add_student(student_name)

# Input dict of courses data is {Course title: list of student name tuples}
courses_data_dict = {"11.1 IB Math SL": imported_roster}

#GLOBAL CREATION OF COURSES DICTIONARY {COURSE TITLE: COURSE INSTANCE}
global_courses_dict = {} # First time only
for course_title in courses_data_dict:
	students = {student:global_students_dict[student] for student in courses_data_dict[course]}
	add_course(course_title, students)

#GLOBAL CREATION OF PROBLEM BANK DICTIONARY {TOPIC: {DIFFICULTY: {ID: INSTANCE}}}
global_problem_dict = {}
for problem in problem_data_dict:
	add_problem()


# PRINT STATEMENTS ARE ONLY TO TEST CODE
if False:
    print(imported_roster)
    print(imported_topics)
    print(imported_skillset)
