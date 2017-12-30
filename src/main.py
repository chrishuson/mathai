#runs worksheet maker functions in an interactive session
# $ python main.py    (from /Users/chris/GitHub/mathai/src directory)
# For Hydrogen
#%pwd
#%cd src

import sys
import os
import csv
import pickle
from collections import namedtuple
from makedoc import makedoc, makeset
from loadstandards import print_tree, loaddbfile, savedbfile

def make_set(problem_ids, pflag=1, sflag=0, wflag=0, numflag=1):
    """ Function to create string of problems in TeX format

        #ids is a list of problem ids, order is maintained
        #flags specify inclusion of problem text, solution & workspace
        #numflag: 1 prefix w "\item", 2 include "\begin{enumerate}"
        Returns tuple of 2 lists: problems' ids, texts (enhance to include set_id)
        """
    problem_texts = []
    for id in problem_ids:
        problem_texts.append(problem[id][0]) #enhance to write solutions, workspace
    return (problem_ids, problem_texts)

def print_set(problem_ids, title, pflag=1, sflag=0, wflag=0, idflag=0, numflag=1):
    """ Creates a worksheet LaTeX file

        problem_ids: list of problem_ids to be included, in order
        title: (out_filename, date, title)
        #flags specify inclusion of problem text, solution & workspace
        idflag: 1 print problem id (enhance for standards & meta info)
        #numflag: 0 - no problem numbers; 1 prefix w "\item" &includes "\begin{enumerate}"
        output file is out_filename.tex in the /out/ directory
        """
    outdir = "/Users/chris/GitHub/mathai/out/"
    dbdir = "/Users/chris/GitHub/mathai/db/"
    outfile = outdir + title[0] + ".tex"

    with open(outfile, "w") as newfile:
        with open(dbdir + "head.tex", "r") as head:
            for line in head:
                newfile.write(line)
        newfile.write(title[1] + r"\\*" + '\n' + r"\begin{center}{" + \
                      title[2] + r"}\end{center}" + '\n')
        #with open(dbdir + "title.tex", "r") as title:
            #for line in title:
                #newfile.write(line)
        if numflag == 1:
            newfile.write(r'\begin{enumerate}' + '\n')

        for id in problem_ids:
            if numflag == 1:
                newfile.write(r'\item ' + problem[id][0])
            else:
                newfile.write(problem[id][0].rstrip("\n")+r'\\*'+'\n')
            if idflag == 1:
                s = str(id) + " " + problem_meta[id][0] + " " +\
                 problem_meta[id][1]
                newfile.write(r'\\' + s + '\n')
            elif idflag == 2:
                newfile.write(r'\marginpar{' + str(id) +r'}' + '\n')

        if numflag == 1:
            newfile.write(r'\end{enumerate}'+'\n')
        with open(dbdir + "foot.tex", "r") as foot:
            for line in foot:
                newfile.write(line)

def print_test():
    """ Runs four configurations of print_set, saving four files
        """
    p = [problem_id for problem_id in problem.keys()]
    p.sort()
    title = ("newfile1", "numflag=0", "Inventory: Full List of Problems")
    print_set(p, title, numflag=0)
    title = ("newfile2", "default (numflag=1)", "Inventory: Full List of Problems")
    print_set(p, title)
    title = ("newfile3", "numflag=1 and idflag=1", "Inventory: Full List of Problems")
    print_set(p, title, idflag=1, numflag=1)
    title = ("newfile4", "numflag=1 and idflag=2", "Inventory: Full List of Problems")
    print_set(p, title, idflag=2, numflag=1)


standards = loaddbfile("standards_tree_jmap")
standards_desc = loaddbfile("standards_text_jmap")
problem = loaddbfile("problem")
problem_meta = loaddbfile("problem_meta")
skill = loaddbfile("skill")


print("running worksheet generator")
arg = input("Type 'all' , 'test', or 'add': ")

if arg == "all":
    p = [problem_id for problem_id in problem.keys()]
    title = ("newfile", "ids in margin", "Inventory: Full List of Problems")
    print_set(p, title, idflag=2)
    print("Done: newfile.tex in out folder.")
elif arg == "test":
    print_test()
    print("Four files newfile*.tex")
elif arg == "add":
    from add import add_problem
    print("add not implemented")
else:
    print("Didn't do anything")
