#add a new problem
# For Hydrogen
#%pwd
#%cd src

from collections import namedtuple
from main import print_set, print_tree, savedbfile, loaddbfile

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

def ccss_lookup(topic):
    for i in range(299, 305):
        if standards[i][2] == topic:
            return standards[i][3]
    return None


standards = loaddbfile("standards_tree_jmap")
standards_desc = loaddbfile("standards_text_jmap")
problem = loaddbfile("problem")
problem_meta = loaddbfile("problem_meta")
skill = loaddbfile("skill")

p_meta_names = "topic, standard, calc_type, difficulty, level, source"
p_meta = namedtuple("p_meta", p_meta_names)

topic = "Inverse of Functions"

standard = ccss_lookup(topic)

p_meta = ("Inverse of Functions",  standard, 1, 3, 1, "cjh")
problem_id = 1200

new_ids = []
indir = "/Users/chris/GitHub/mathai/in/"
filename = indir + "add.txt"
with open(filename, "r") as add_file:
    problemlist = []
    for line in add_file:
        l = line.lstrip("\\item ")
        #Careful! This will strip any of these letters, not just the prefix
        problemlist.append(l)

for problem_text in problemlist:
    n = add_problem(problem_id, p_meta, problem_text)
    print(n)
    new_ids.append(n)

print(new_ids)

#p = [problem_id for problem_id in problem.keys()]
title = ("new_probs", "ids in margin", "Inventory: New Problems")
print_set(new_ids, title, idflag=2)


savedbfile(problem, "problem3")
savedbfile(problem_meta, "problem_meta3")
savedbfile(skill, "skill3")
