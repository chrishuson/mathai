import sys
import os

HOME = os.environ["HOME"]

def sayhi(msg='sayhi'):
    """ Prints given argument or 'sayhi' by default.
        """
    print(msg)


print('hello world')

for i in range(5):
    print('i equals ', i)

    #print('post breakpoint')

x = 7
tempmsg = 'temporary msg'
#print('temp variable equals ', temp)
print('finished running')

tempmsg

def summary(global_problem_dict):
    print('topic, difficulty, problemid, len of question text')
    c = 0
    for t in global_problem_dict:
        for d in global_problem_dict[t]:
            for pid in global_problem_dict[t][d]:
                c += 1
                print(c, t, d, pid, '    ', end='')
                try:
                    print('len: ', len(global_problem_dict[t][d][pid].texts['question']))
                except:
                    print('error getting texts.question')
                    continue