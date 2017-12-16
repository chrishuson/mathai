#requires standards.txt list of files to load and
# associated problem files with .tex endings, in /tex subdirectory
def loadbank(standards):
    """returns data store of exercises, dict standard:problemlist

        list of strings defining problem groups
        dictionary of string:lists, returned with problems from files"""
    problemdir = "/Users/chris/mathai/tex/"
    bank = {}
    for standard in standards:
        filename = problemdir + standard + ".tex"
        problems = open(filename, "r")
        problemlist = []
        for line in problems:
            problemlist.append(line)
        bank[standard] = problemlist
    return bank

#first load the standards file names
def loadstandards():
    """Load list of standards from config file, standards.txt in tex/"""
    standardsdir = "/Users/chris/mathai/tex/"
    filename = standardsdir + "standards.txt"
    standardsfile = open(filename, "r")
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
