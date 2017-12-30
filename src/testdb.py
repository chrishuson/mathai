#test procedure of pickle db functions
import pickle
from loadbank import loadstandards, loadbank
from bankdb import savebank, loaddb
from loadstandards import loaddbfile, print_tree

def testsave():
    standards = loadstandards()
    bank = loadbank(standards)
    savebank(bank)
    print("saved bank.pickle db file")

def testload():
    return loaddb("bank")

for id in problem_meta.keys():
    print(problem_meta[id][0][:12],problem_meta[id][1], problem_meta[id][2], \
          problem_meta[id][3], problem_meta[id][4])

#run only if module is called from command line
if __name__ == "__main__":
    from loadbank import loadstandards, loadbank
    from bankdb import savebank, loaddb
    print("Test pickle file saving functions")
    prompt = input("Type 's' to create and save problem bank. \
                   'r' to retrieve and print problem bank. \
                   'd' standards descriptions. 't' for tree: ")
    if prompt == 's':
        testsave()
    elif prompt == 'r':
        print("bank.pickle : ", testload())
    elif prompt == 'd':
        d = loaddbfile("standards_text_jmap")
        print("standards_text_jmap")
        for k in d.keys():
            print(k)
            print(d[k])
    else:
        t = loaddbfile("standards_tree_jmap")
        print_tree(t)


#for dir in sys.path:
#    print(dir)
