#runs worksheet maker functions in an interactive session
# $ python main.py    (from /Users/chris/GitHub/mathai/src directory)
import sys
import os
import csv
import pickle
from collections import namedtuple
from makedoc import makedoc, makeset
from loadstandards import print_tree, loaddbfile

problem_set = {}
    #set_id:(problem_ids, string), text composing problems in TeX format

def make_set(problem_ids, pflag=1, sflag=0, wflag=0, numflag=1):
    """ Function to create string of problems in TeX format

        #ids is a list of problem ids, order is maintained
        #flags specify inclusion of problem text, solution & workspace
        #numflag: 1 prefix w "\item", 2 include "\begin{enumerate}"
        Returns list of problems' texts (enhance to include set_id)
        """
    problem_texts = []
    for id in problem_ids:
        problem_texts.append(problem[id][0]) #enhance to write solutions, workspace
    return (problem_ids, problem_texts)

def print_set(set_tuple, idflag=0, numflag=1):
    """ Creates a worksheet LaTeX file

        set_tuple (list of problem_ids, list of problems' texts)
        idflag: 1 print problem id (enhance for standards & meta info)
        #numflag: 1 prefix w "\item", 2 includes "\begin{enumerate}"
        output files are in the /out/ directory
        """
    outdir = "/Users/chris/GitHub/mathai/out/"
    dbdir = "/Users/chris/GitHub/mathai/db/"
    outfile = outdir + "newfile.tex"
    with open(outfile, "w") as newfile:
        with open(dbdir + "head.tex", "r") as head:
            for line in head:
                newfile.write(line)
        with open(dbdir + "title.tex", "r") as title:
            for line in title:
                newfile.write(line)
        if numflag == 1:
            newfile.write(r'\begin{enumerate}'+'\n')
        for index in range(len(set_tuple[1])):
            if idflag == 1:
                newfile.write(set_tuple[0][index])
            newfile.write(set_tuple[1][index])

        if numflag == 1:
            newfile.write(r'\end{enumerate}'+'\n')

        with open(dbdir + "foot.tex", "r") as foot:
            for line in foot:
                newfile.write(line)


#bank = loaddbfile("bank")
standards = loaddbfile("standards_tree_jmap")
standards_desc = loaddbfile("standards_text_jmap")
problem = loaddbfile("problem")
problem_meta = loaddbfile("problem_meta")
skill = loaddbfile("skill")


print("running worksheet generator")
arg = input("Type anything to run: ")

p = [1204, 1205, 1206, 1207]
#set_tuple = (p, make_set(p))
#print(set_tuple)
print_set(make_set(p))

#standards = loadstandards()
#bank = loadbank(standards)
#makedoc(bank)

print("done. look for newfile.tex in out folder")

#for dir in sys.path:
#    print(dir)
