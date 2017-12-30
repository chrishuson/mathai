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
#from add import add_problem

def savedbfile(dbfile, filename):
    """Saves persistent record using pickle

        dbfile - to be saved (problem records, standards files)
        filename -  filename.pickle in /Users/chris/GitHub/mathai/db
         ("bank", "standards_text_jmap", "standards_tree_jmap")
        """
    dbdir = "/Users/chris/GitHub/mathai/db/"
    p = dbdir + filename + '.pickle'
    with open(p, 'wb') as f:
        pickle.dump(dbfile, f, pickle.HIGHEST_PROTOCOL)

def loaddbfile(filename):
    """Retrieves persistent record using Pickle

        filename -  filename.pickle in /Users/chris/GitHub/mathai/db
         ("bank", "standards_text_jmap", "standards_tree_jmap")
        (problem records, standards files)
        """
    dbdir = "/Users/chris/GitHub/mathai/db/"
    p = dbdir + filename + '.pickle'
    with open(p, 'rb') as f:
        return pickle.load(f)


def print_tree(s):
    """Print out nested list of standardsdir

        s is a list of 4-tuples, i.e. the standards data structure
        """
    print(s[0][0])
    print("   " + s[0][1])
    print("      " + s[0][2] + "  " + s[0][3])
    for i in range(1,len(s)):
        if not s[i-1][0] == s[i][0]:
            print(s[i][0])
            print("   " + s[i][1])
            print("      " + s[i][2] + "  " + s[i][3])
        elif not s[i-1][1] == s[i][1]:
            print("   " + s[i][1])
            print("      " + s[i][2] + "  " + s[i][3])
        elif not s[i-1][2] == s[i][2]:
            print("      " + s[i][2] + "  " + s[i][3])
        elif not s[i-1][3] == s[i][3]:
            print("                       " + s[i][3])


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

#run only if module is called from command line
if __name__ == "__main__":
    print("running worksheet generator")
    arg = input("Type 'all' , 'test', 'tree' or 'add': ")

    if arg == "all":
        p = [problem_id for problem_id in problem.keys()]
        title = ("newfile", "ids in margin", "Inventory: Full List of Problems")
        print_set(p, title, idflag=2)
        print("Done: newfile.tex in out folder.")
    elif arg == "test":
        print_test()
        print("Four files newfile*.tex")
    elif arg == "tree":
        print_tree(standards)
    elif arg == "add":
        from add import add_problem
        print("add not implemented")
    else:
        print("Didn't do anything")
