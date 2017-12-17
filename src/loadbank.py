#requires standards.txt list of files to load and
# associated problem files with .tex endings, in /db subdirectory
def loadbank(standards):
    """returns data store of exercises, dict standard:problemlist

        argument - list of strings defining problem groups by file name
        returns - dictionary of string:lists, list of problems from files"""
    problemdir = "/Users/chris/GitHub/mathai/db/"
    bank = {}
    for standard in standards:
        filename = problemdir + standard + ".tex"
        with open(filename, "r") as problems:
            problemlist = []
            for line in problems:
                problemlist.append(line)
        bank[standard] = problemlist
    return bank

#first load the standards file names
def loadstandards():
    """Load list of standards from config file, standards.txt in ./db/"""
    standardsdir = "/Users/chris/GitHub/mathai/db/"
    filename = standardsdir + "standards.txt"
    with open(filename, "r") as standardsfile:
        standards = []
        for line in standardsfile:
            standards.append(line[0:-1]) #strip new lines at end of each filename string
    return standards

#run only if module is called from command line
if __name__ == "__main__":
    import sys
    standards = loadstandards()
    bank = loadbank(standards)
    print(bank)
