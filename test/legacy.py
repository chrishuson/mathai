
import sys
import os
import csv
import pickle
from collections import namedtuple

from class_organization import ProblemSet, DifferentiatedProblemSet, Assessment, \
                                Problem, Course, Student, assign_problem_set

HOME = os.environ["HOME"]
dbdir = HOME + "/GitHub/mathai/db/"
outdir = HOME + "/GitHub/mathai/out/"
indir = HOME + "/GitHub/mathai/in/"
