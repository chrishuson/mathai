#add a new problem
from collections import namedtuple

def add_problem(prob_id, p_meta, prob_text):
    """ Appends and saves to pickle files new problem_meta

        prob_id: taken as starting point, if duplicate, increments
        p_meta: tuple of "topic, standard, calc_type, difficulty, level, source"
        prob_text: TeX format problem text (add solution and workspace)
        return actual problem_id number
        """



p_meta_names = "topic, standard, calc_type, difficulty, level, source"
p_meta = namedtuple("p_meta", p_meta_names)


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
