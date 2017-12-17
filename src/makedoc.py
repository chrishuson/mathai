#makes tex document
#standard input files are fixed '.tex' head, title, and foot
#bank is a dictionary of standards and associated lists of problems
#worksheet1.csv configures the type and number of problems, the section title
#run command from terminal in root directory is
#   python GitHub/mathai/src/makedoc.py
def makeset(standard, s, n, bank):
    """Returns a list of problems for one standard

        standard is the string label of the problem type
        n is the number of problem lines returned in a list
        s is the number of the first one, counting from zero
        bank is the dictionary of problems"""
    problempick = []
    problemlist = bank[standard]
    m = len(problemlist) #these 3 lines fix arguments outside the bounds of bank
    s = min(s, m-1)
    n = min(n, m-s)
    for i in range(s, s+n):
        problempick.append(problemlist[i])
    return problempick

def makedoc(bank):
    """Creates a worksheet LaTeX file

        bank is dictionary of exercises, standard:problemlist
        output files are in the /out/ directory """
    outdir = "/Users/chris/GitHub/mathai/out/"
    dbdir = "/Users/chris/GitHub/mathai/db/"
    outfile = outdir + "newfile.tex"
    with open(outfile, "w") as newfile:
        with open(dbdir + "head.tex", "r") as head:
            for line in head:
                newfile.write(line)
        with open(dbdir + "title.tex", "r") as title:
            for line in title:
                newfile.write(line)
        newfile.write(r'\begin{enumerate}'+'\n') #problem section to begin and end with enumerate

        #problem section
        with open(dbdir + "worksheet1.csv", "r") as f:
            #worksheet comma-separated columns: standard, 1st prob,
            #number of problems, string to be used a subsection title
            for line in f:
                line = line.split(",") #this long preprocessing could be compressed
                standard, s, n, section = line
                s = int(s)
                n = int(n)
                section = section.lstrip()
                section = section.rstrip('\n')
                newfile.write(r'\subsection*{'+ section +r'}'+'\n')
                problemset = makeset(standard, s, n, bank) #call makeset here
                for problem in problemset:
                    newfile.write(problem)

        newfile.write(r'\end{enumerate}'+'\n') #problem section to end with enumerate

        with open(dbdir + "foot.tex", "r") as foot:
            for line in foot:
                newfile.write(line)

#run only if module is called from command line
if __name__ == "__main__":
    from quickbank import quickbank
    bank = quickbank()
    makedoc(bank)
