# Suite of functions to test functions in main.py
# 

import os

from class_organization import Problem, ProblemSet

HOME = os.environ["HOME"]
dbdir = HOME + "/GitHub/mathai/test/db/"
outdir = HOME + "/GitHub/mathai/test/out/"
indir = HOME + "/GitHub/mathai/test/in/"


def make_test_problem_db():
    test_problem_db = {}
    test_problem_db[1] = Problem(1, 'unassigned', {'question':'text for problem number 3 \nwith a second line'}, 'Arc Length', 4, 5, 0, 'test')
    test_problem_db[2] = Problem(2, 'Area of Circles', {'question':'more text for problem number 3 \nwith a second line'}, 'Sector', 4, 5, 0, 'test')
    test_problem_db[3] = Problem(3, 'unassigned', {'question':'even more text for problem number 3 \nwith a second line'}, 'Arc Length', 4, 5, 0, 'test')
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
    test_problem_db = unit_tests.make_test_problem_db() #delete module prefix
    test_problem_set_db = {1: unit_tests.make_problem_set()} #


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
                for problem_id in global_problem_dict[topic][difficulty]:
                    print(topic, difficulty, problem_id)
                    #print(global_problem_dict[topic][difficulty][id].tex(1))

    return comments