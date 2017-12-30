#add a new problem
from collections import namedtuple
from loadstandards import savedbfile, loaddbfile


def add_problem(problem_id, p_meta, problem_text):
    """ Appends and saves to pickle files new problem_meta

        prob_id: taken as starting point, if duplicate, increments
        p_meta: tuple of "topic, standard, calc_type, difficulty, level, source"
        prob_text: TeX format problem text (add solution and workspace)
        return actual problem_id number
        """
    while problem_id in problem.keys():
        problem_id +=  1
    problem[problem_id] = [problem_text] #solution and workspace add later
    #p_meta = (lookup_list[tmp], lookup_ccss(lookup_list[tmp]), 1, 3, 1, "cjh")
    problem_meta[problem_id] = p_meta
    skill[p_meta[0]].append(problem_id)
    return problem_id


standards = loaddbfile("standards_tree_jmap")
standards_desc = loaddbfile("standards_text_jmap")
problem = loaddbfile("problem")
problem_meta = loaddbfile("problem_meta")
skill = loaddbfile("skill")

p_meta_names = "topic, standard, calc_type, difficulty, level, source"
p_meta = namedtuple("p_meta", p_meta_names)
p_meta = ("Evaluating Exponential Expressions", "F.IF.B.4", 1, 3, 1, "cjh")
problem_id = 1000

indir = "/Users/chris/GitHub/mathai/in/"
filename = indir + "add.txt"
with open(filename, "r") as problems:
    problemlist = []
    for line in problems:
        problemlist.append(line)

for problem_text in problemlist:
    n = add_problem(problem_id, p_meta, problem_text)
    print(n)

savedbfile(problem, "problem2")
savedbfile(problem_meta, "problem_meta2")
savedbfile(skill, "skill2")
