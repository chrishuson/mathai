# Suite of functions to test functions in main.py
# 

import os

from crawler import parsebody, parsetexfile
from class_organization import Problem, ProblemSet

HOME = os.environ["HOME"]
dbdir = HOME + "/GitHub/mathai/test/db/"
outdir = HOME + "/GitHub/mathai/test/out/"
indir = HOME + "/GitHub/mathai/test/in/"


def make_test_problem_db():
    test_problem_db = {}
    test_problem_db[1] = Problem(1, 'unassigned', {'question':'text for problem number 1 \nwith a second line'}, 'Arc Length', 4, 5, 0, 'test')
    test_problem_db[2] = Problem(2, 'Area of Circles', {'question':'more text \nThis problem (\\#2) has \nthree lines'}, 'Sector', 4, 5, 0, 'test')
    test_problem_db[3] = Problem(3, 'unassigned', {'question':'Problem text for problem number 3 \nwith a second line'}, 'Arc Length', 4, 5, 0, 'test')
    return test_problem_db


def make_problem_set(problem_set_id=1):
    test_problem_db = make_test_problem_db()
    problems = [test_problem_db[problem_id] for problem_id in test_problem_db]
    spacing = []
    title = ('1.1 Test Worksheet title', '17 July 2019', 'Unit testing - print functionality')
    course_title = '11.1 IB Math SL'
    unit = 'powers'
    return ProblemSet(problem_set_id, problems, spacing, title, course_title, unit)

def make_suite():
    test_problem_db = make_test_problem_db()
    test_problem_set_db = {1: make_problem_set()}
    print('Returning test problem_db and problem_set_db dicts')
    return test_problem_db, test_problem_set_db


def test_problem_tex(problem_db=None, #TODO fails for empty problem_db
            title=('My Worksheet title', '7/16/2019', '3rd string in title')):
    """ Prints various configurations of the class problems' tex output string

        problem_db - dict, of Problem instances to run the test on. 
        title - 3-tuple, strings of worksheet title, date, comment
        """
    for problem_id in problem_db:
        print('cycle for problem_id = ', problem_id)
        print('#1 arguments: ', 'no function arguments')
        print(problem_db[problem_id].tex())
        print('#2 arguments: ', 'meta=True')
        print(problem_db[problem_id].tex(meta=True))
        print('#3 arguments: ', "question=False, meta=True, head='short extra'")
        print(problem_db[problem_id].tex(question=False, meta=True, head='short extra'))
        print('#4 arguments: ', 'naked=False, numflag=True')
        print(problem_db[problem_id].tex(naked=False, numflag=True))
        print('#5 runs make_tex_head with no arguments')
        print(problem_db[problem_id].make_tex_head())
        print('#6 runs make_tex_head with given title tuple argument')
        print(problem_db[problem_id].make_tex_head(title=title))


def test_parse(testtitles=None):
    """ Uploads tex file, parses it into sections then problems

        testtitles - list of title tuples, each containing (filename, date, worksheet title)
        returns 5-tuple of intermediate results: problems, spacing, packages, header, body
        """
    if testtitles is None:
        testtitles = []
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

def test_global_load(long = False): #Doesn't work because can't see variables in main
    """ Several short commands to confirm key data has loaded properly

        """
    comments = []
    global standards
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
                for problem_id in global_problem_dict[topic][difficulty]:
                    print(topic, difficulty, problem_id)
                    #print(global_problem_dict[topic][difficulty][id].tex(1))

    return comments