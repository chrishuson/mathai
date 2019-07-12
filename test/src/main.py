#runs worksheet maker functions in an interactive session
# $ python main.py    (from /Users/chris/GitHub/mathai/src directory)


import sys
import os
import csv
import pickle
from collections import namedtuple

from class_organization import ProblemSet, DifferentiatedProblemSet, Assessment, \
                                Problem, Course, Student, assign_problem_set
#import test


HOME = os.environ["HOME"]
dbdir = HOME + "/GitHub/mathai/db/"
outdir = HOME + "/GitHub/mathai/out/"
indir = HOME + "/GitHub/mathai/in/"

testflag = True
if testflag:
    dbdir = HOME + "/GitHub/mathai/test/db/"
    outdir = HOME + "/GitHub/mathai/test/out/"
    indir = HOME + "/GitHub/mathai/test/in/"


def savedbfile(dbfile, filename):
    """ Saves persistent record using pickle

        dbfile - to be saved (problem records, standards files)
        filename -  filename.pickle in ~/GitHub/mathai/db
         ("bank", "standards_text_jmap", "standards_tree_jmap")
        """
    p = dbdir + filename + '.pickle'
    with open(p, 'wb') as f:
        pickle.dump(dbfile, f, pickle.HIGHEST_PROTOCOL)


def loaddbfile(filename):
    """ Returns persistent record that was saved with pickle

        filename -  filename.pickle in ~/GitHub/mathai/db
         ("bank", "standards_text_jmap", "standards_tree_jmap")
        (problem records, standards files)
        """
    p = dbdir + filename + '.pickle'
    try:
        with open(p, 'rb') as f:
            return pickle.load(f)
    except FileNotFoundError:
        print('Tried to open non-existent file: ' + p)


def save_global_files():
    """ Placeholder function for pickle save commands
        """
    savedbfile(global_courses_dict, "global_courses_dict")
    savedbfile(global_students_dict, "global_students_dict")
    savedbfile(global_problem_dict, "global_problem_dict")
    savedbfile(global_problemset_dict, "global_problemset_dict")


def lookup_new_problem_id(topic, difficulty = 3):
    """ Selects an unused integer for use as key in the global_problem_dict
            
        topic - str, in keys of topic_ids file/dictionary. eg "Inverse of Functions"
        difficulty - int
        The topic and difficulty args are mapped to a starting place based on
        giving each topic a thousand ids.
        """
    topic_ids = loaddbfile("topic_ids")
    existing_problem_ids = set()
    for t in global_problem_dict:
        for d in global_problem_dict[t]:
            for id in global_problem_dict[t][d]:
                existing_problem_ids.add(id)
    seed = 1
    #print(topic, difficulty, seed, len(existing_problem_ids))
    if topic in topic_ids.keys():
        seed = int(topic_ids[topic]) + int(difficulty) * 100
    while seed in existing_problem_ids:
        seed += 1
    return seed


def lookup_standard(topic):
    """ Return the CCSS standard number for a given problem topic
        """
    standards = loaddbfile("standards_tree_jmap")
    # list of 4-tuples, (course, chapter, topic, ccss number) from JMAP
    for i in range(0,len(standards)):
        if standards[i][2] == topic:
            return standards[i][3]
    return None


def print_tree(s):
    """ Print out nested list of standardsdir

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


def print_standards_descriptions(standards_desc):
    """ Prints the CCSS number and its text description, one per line.

        standards_desc is a dict, {ccss number, text description} from JMAP
        """
    for s in standards_desc.keys():
        print(s + " " + standards_desc[s])

def print_problemset(problem_ids, title, pflag=1, sflag=0, wflag=0, idflag=0, numflag=1):
    """ Creates a worksheet LaTeX file

        problem_ids: list of problem_ids to be included, in order
        title: (out_filename, date, title)
        #flags specify inclusion of problem text, solution & workspace
        idflag: 1 print problem id (enhance for standards & meta info)
        #numflag: 0 - no problem numbers; 1 prefix w "\item" &includes "\begin{enumerate}"
        output file is out_filename.tex in the /out/ directory
        """
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


def print_set_legacy(problem_ids, title, pflag=1, sflag=0, wflag=0, idflag=0, numflag=1):
    """ Creates a worksheet LaTeX file

        problem_ids: list of problem_ids to be included, in order
        title: (out_filename, date, title)
        #flags specify inclusion of problem text, solution & workspace
        idflag: 1 print problem id (enhance for standards & meta info)
        #numflag: 0 - no problem numbers; 1 prefix w "\item" &includes "\begin{enumerate}"
        output file is out_filename.tex in the /out/ directory
        """
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



def parsetexfile(infile):
    """ divide tex file into three sections
    
        infile - str, full directory name of file
        returns tuple of three lists of text lines:
        the top packages section, header lines, and body text
        """
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
    """ Parses the body of a tex problem set into separate problems
        
        body - list of text lines
        returns - problems: list of problem strings
            spacing: list of section and formatting text lines
        """
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
            if nested:
                nested = False
                problem.append(line)
            else:
                spacing.append(line)
                problems.append(problem)
                problem = []
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
    #print(problems)
    empty = []
    while True:
        try: 
            problems.remove(empty)
        except:
            break
    trimmedproblems = [trim_item_prefix(problem) for problem in problems]
    problemstextblock = [''.join(problem) for problem in trimmedproblems]
    return problemstextblock, spacing

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


def import_students_from_files(course_title = "11.1 IB Math SL"):
    """ Upload student (& skills) data from text files in indir

        internal data structures:
        imported_topics - list, for problemset and skillset
        imported_roster - list of tuples [(last, first_name), ...], into course & student global dicts
        imported_skillset {student: {topic: int 0-10}}
        course_title - str, for global_courses_dict
        """
    # IMPORT INITIAL BATCH OF TOPICS AS LIST OF TEXTS, called imported_topics
    infile = indir + "skillset_topics.csv"
    imported_topics = []
    with open(infile, "r", encoding='latin-1') as topics_file:
        f = csv.reader(topics_file, delimiter=',', quotechar='"')
        for row in f:
            imported_topics.append(row[0])
    # Fix corruption of first character of first imported topics
    imported_topics[0] = "Modeling Exponential Functions"

    # IMPORT INITIAL ROSTER AND SKILLSETS, imported_roster [] and imported_skillset {}
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

    #GLOBAL CREATION OF STUDENTS DICTIONARY {STUDENT NAME TUPLE: STUDENT INSTANCE}
    for student in imported_roster:
        global_students_dict[student] = Student(student)
        global_students_dict[student].skillset = imported_skillset.get(student)

    courses_data_dict = {course_title: imported_roster}
    #GLOBAL CREATION OF COURSES DICTIONARY {COURSE TITLE: COURSE INSTANCE}
    for course_title in courses_data_dict:
    	students = {student:global_students_dict[student] for student in courses_data_dict[course_title]}
    global_courses_dict[course_title] = Course(course_title, students)

    # PRINT STATEMENTS ARE ONLY TO TEST CODE
    if False:
        print(imported_roster)
        print(imported_topics)
        print(imported_skillset)

def import_problems_from_files():
    """ Upload problems from indir problems files

        problems.csv - flatfile, fields: Topic,Difficulty,Calculator,Level,Text,Resource,Instructions
        """
    # IMPORT PROBLEMS AND SET UP FOR DEC 14 PROBLEM SET as imported_problems {}
    # INFILE
    infile = indir + "problems.csv"
    i = 0
    with open(infile, "r", encoding='latin-1') as r_file:
        f = csv.reader(r_file, delimiter=',', quotechar='"')
        for row in f:
            print(i)
            i += 1
            topic = row[0]
            standard = lookup_standard(topic)
            difficulty = row[1]
            calculator = row[2]
            level = row[3]
            question = row[4]
            resource = row[5]
            instructions = row[5]
            texts = {"question": question, "resource": resource, "instructions": instructions}
            source = "cjh"
            problem_id = lookup_new_problem_id(topic, difficulty)
                #NOT YET IMPORTED: workspace, answer, solution, rubric
            global_problem_dict[topic] = {difficulty: {problem_id: \
                Problem(topic, texts, standard, difficulty, level, calculator, source)}}

    # DELETE ENTRY WITH CORRUPT KEY FROM FIRST (TITLE) ROW IN IMPORTED FILE
    for topic in global_problem_dict:
        if topic[-3:] == "pic":
            del global_problem_dict[topic]


def refresh_problem_dict_all_all():
    """ Loop through the global_problem_dict to make a universal dictionary under ["all"][0]

        Makes it easy to lookup instance from problem id.
        I INTEND FOR THIS TO BE A SHALLOW COPY
        """
    global global_problem_dict
    for topic in global_problem_dict:
        if topic != "all":
            for difficulty in global_problem_dict[topic]:
                if difficulty != "all":
                    for id in global_problem_dict[topic][difficulty]:
                        global_problem_dict["all"]["all"][id] = global_problem_dict[topic][difficulty][id]


def make_problem_set(date_id):
    """ function Placeholder
        """
    p_ids = [46500, 59300, 167300, 159300, 61200, 178300, 74300, 42500, 60400, 73300]
    problem_ids = {'general': p_ids, ('last','first'): p_ids[1:5]} #Problemsets have problem_id lists by student
    unit = "powers"
    course_title = "11.1 IB Math SL"
    global global_problemset_dict
    global_problemset_dict[course_title] = {unit: {date_id:ProblemSet(course_title, unit, problem_ids)}}
    global_problemset_dict["all"]["all"][date_id] = global_problemset_dict[course_title][unit][date_id]


def print_test():
    """ Runs four configurations of print_set, saving four files
        """
    p = [problem_id for problem_id in problem.keys()] # WHY DOESN'T PROBLEM NEED TO BE GLOBAL?
    p.sort()
    title = ("newfile1", "numflag=0", "Inventory: Full List of Problems")
    print_set_legacy(p, title, numflag=0)
    title = ("newfile2", "default (numflag=1)", "Inventory: Full List of Problems")
    print_set_legacy(p, title)
    title = ("newfile3", "numflag=1 and idflag=1", "Inventory: Full List of Problems")
    print_set_legacy(p, title, idflag=1, numflag=1)
    title = ("newfile4", "numflag=1 and idflag=2", "Inventory: Full List of Problems")
    print_set_legacy(p, title, idflag=2, numflag=1)


def test_global_load(long = False):
    """ Several short commands to confirm key data has loaded properly

        """
    comments = []
    if len(standards) != 0:
        comments.append(str(len(standards)) + " standards")
    else:
        comments.append("Error with standards")

    if len(standards_desc) != 0:
        comments.append(str(len(standards_desc)) + " standards_desc")
    else:
        comments.append("Error with standards_desc")

    if len(topic_ids) != 0:
        comments.append(str(len(topic_ids)) + " topic_ids")
    else:
        comments.append("Error with topic_ids")

    if len(global_courses_dict) != 0:
        comments.append(str(len(global_courses_dict)) + " courses")
    else:
        comments.append("Error with courses")

    if len(global_students_dict) != 0:
        comments.append(str(len(global_students_dict)) + " students")
    else:
        comments.append("Error with students")

    if len(global_problem_dict) != 0:
        comments.append(str(len(global_problem_dict)) 
            + " problem topics in global_problem_dict")
    else:
        comments.append("Error with problems")

    if len(global_problemset_dict) != 0:
        comments.append(str(len(global_problemset_dict)) + " problem sets")
    else:
        comments.append("Error with problem sets")

    if long:
        for course_title in global_courses_dict:
            print('Roster follows for course: ' + course_title)
            global_courses_dict[course_title].print_roster()
        print(global_problem_dict)
        for topic in global_problem_dict:
            for difficulty in global_problem_dict[topic]:
                for id in global_problem_dict[topic][difficulty]:
                    print(topic, difficulty, id)
                    #print(global_problem_dict[topic][difficulty][id].format(1))

    return comments


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

"""
if False:
    print(test_global_load(1))
    #legacy loading steps
    problem = loaddbfile("problem") #TODO MIGRATE THIS TO global_problem_dict
    # dict of problems, {id:[problem text, solution text, workspace text]}
    problem_meta = loaddbfile("problem_meta") #TODO MIGRATE THIS TO global_problem_dict
    # dict of problem information {id:(topic, standard, calc_type=1, difficulty=3,
    #                                  level=1, source='cjh')
    # calc_type: 0 no calculator allowed, 1 allowed, 2 calc practice
    # difficulty 1-10
    # level 1-6 (webworks reference)
    # source - author, or history of exercise ("cjh")
    skill = loaddbfile("skill") #TODO MIGRATE THIS TO global_problem_dict
    # dict of problem ids for each topic, {topic:[id1, id2, ...]}"""

standards = loaddbfile("standards_tree_jmap")
# list of 4-tuples, (course, chapter, topic, ccss number) from JMAP
standards_desc = loaddbfile("standards_text_jmap")
# dict of text descriptions of standards, {ccss number, description} from JMAP
topic_ids = loaddbfile("topic_ids")
# dict {topic: starting problem_id number} 1000 for each of 233 topics

topic_ids['unassigned']=0

global_courses_dict = loaddbfile("global_courses_dict")
#GLOBAL COURSES DICTIONARY {COURSE TITLE: COURSE INSTANCE}
global_students_dict = loaddbfile("global_students_dict")
#GLOBAL STUDENTS DICT {STUDENT NAME TUPLE: STUDENT INSTANCE}
global_problem_dict = loaddbfile("global_problem_dict")
#GLOBAL PROBLEM DICT {TOPIC: {DIFFICULTY: {ID: INSTANCE}}} {'unassigned':{0:{}}}
global_problemset_dict = loaddbfile("global_problemset_dict")
# GLOBAL PROBLEM SET DICT {COURSE: {UNIT: {ID: INSTANCE}}}

#run only if module is called from command line
if __name__ == "__main__":
    print("running worksheet generator")
    arg = input("Type 'all' , 'test', 'tree', 'desc', or 'add': ")

    if arg == "all":
        p = [problem_id for problem_id in problem.keys()]
        title = ("newfile", "ids in margin", "Inventory: Full List of Problems")
        print_set_legacy(p, title, idflag=2)
        print("Done: newfile.tex in out folder.")
    elif arg == "test":
        print_test()
        print("Four files newfile*.tex")
    elif arg == "tree":
        print_tree(standards)
    elif arg == "desc":
        print_standards_descriptions(standards_desc)
    elif arg == "add":
        # from add import add_problem  -- LEGACY
        print("add not implemented")
    else:
        print("Didn't do anything")
