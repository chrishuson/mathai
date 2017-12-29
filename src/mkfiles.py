# This is a one-time utility to migrate the previous problems in bank.py to
# new problem files. (problem, skill, and problem_meta)
from collections import namedtuple
from makedoc import makedoc, makeset
from loadstandards import print_tree, loaddbfile, savedbfile

def lookup_ccss(topic):
    """ Returns the ccss alphanumeric code associated with the jmap topics.

        topic - string from standards[2] tuples
        returns NONE if string is not found (there are many inaccuracies in this lookup)
        """
    for node in standards:
        if node[2] == topic:
            return node[3]

bank = loaddbfile("bank")
standards = loaddbfile("standards_tree_jmap")
standards_desc = loaddbfile("standards_text_jmap")

tmp_list = ['exponents', 'logs', \
            'function-inverse', 'substitution', \
            'exponent-fin']  # 'g-quad-vertex',
new_list = ['Evaluating Exponential Expressions', 'Evaluating Logarithmic Expressions', \
            'Inverse of Functions', 'Evaluating Expressions',  \
            'Exponential Equations, Exponential Growth, Exponential Decay']
                #'Graphing Quadratic Functions',

lookup_list = dict(zip(tmp_list, new_list))

problem_id = 1000
problem = {}
problem_meta = {}
p_meta_names = "topic, standard, calc_type, difficulty, level, source"
p_meta = namedtuple("p_meta", p_meta_names)
skill = {}
for k in new_list:
    skill[k] = []

for tmp in lookup_list: # loop through standards in bank
    for prob_text in bank[tmp]: # loop through problems for each old standard
        while problem_id in problem.keys():
            problem_id +=  1
        problem[problem_id] = [prob_text] #solution and workspace add later
        p_meta = (lookup_list[tmp], lookup_ccss(lookup_list[tmp]), 1, 3, 1, "cjh")
        problem_meta[problem_id] = p_meta
        skill[lookup_list[tmp]].append(problem_id)
    problem_id +=  100


savedbfile(problem, "problem")
savedbfile(problem_meta, "problem_meta")
savedbfile(skill, "skill")

p = loaddbfile("problem")
print(p)
m = loaddbfile("problem_meta")
print(m)
s = loaddbfile("skill")
print(s)

#run only if module is called from command line
#if __name__ == "__main__":
    #print(bank.keys())
