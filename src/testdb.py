#test procedure of pickle db functions
from loadbank import loadstandards, loadbank
from bankdb import savebank, loaddb

def testsave():
    standards = loadstandards()
    bank = loadbank(standards)
    savebank(bank)
    print("saved bank.pickle db file")

def testload():
    return loaddb("bank")


#run only if module is called from command line
if __name__ == "__main__":
    from loadbank import loadstandards, loadbank
    from bankdb import savebank, loaddb
    prompt = input("Type 's' to create and save test bank to pickle file. \
                   Else retrieve and print bank.:")
    if prompt == 's':
        testsave()
    else:
        print("bank.pickle : ", testload())
