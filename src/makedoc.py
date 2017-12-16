#makes tex document
#standard input files are fixed '.tex' head, title, and foot
#bank is a dictionary of standards and associated list of problems
#worksheet1.csv configures the type and number of problems, the section title
#run command from terminal in root directory is
#   python mathai/makedoc.py
def makeset(standard, s, n, bank):
    """standard is the string label of the problem type
        n is the number of problem lines returned in a list
        first is the number of the first one, starting w zero
        bank is the dictionary of problems"""
    problempick = []
    problemlist = bank[standard]
    m = len(problemlist)
    s = min(s, m-1)
    n = min(n, m-s)
    for i in range(s, s+n):
        problempick.append(problemlist[i])
    return problempick

def makedoc(bank):
    """Creates a worksheet LaTeX file

        argument bank is dictionary of standard:problemlist"""
    newfile = open("/Users/chris/mathai/tex/newfile.tex", "w")
    head = open("/Users/chris/mathai/tex/head.tex", "r")
    for line in head:
        newfile.write(line)

    title = open("/Users/chris/mathai/tex/title.tex", "r")
    for line in title:
        newfile.write(line)

    newfile.write(r'\begin{enumerate}'+'\n') #problem section to begin and end with enumerate

    #problem section
    f = open("/Users/chris/mathai/tex/worksheet1.csv", "r")
    for line in f:
        lst=line.split(",") #this long preprocessing could be compressed
        standard = lst[0]
        s = int(lst[1])
        n = int(lst[2])
        section = lst[3]
        section = section.lstrip()
        section = section.rstrip('\n')
        newfile.write(r'\subsection*{'+ section+r'}'+'\n')
        problemset = makeset(standard, s, n, bank) #call makeset here
        for problem in problemset:
            newfile.write(problem)
    f.close()

    newfile.write(r'\end{enumerate}'+'\n') #problem section to begin and end with enumerate

    foot = open("/Users/chris/mathai/tex/foot.tex", "r")
    for line in foot:
        newfile.write(line)
    newfile.close()

#run only if module is called from command line
if __name__ == "__main__":
    from quickbank import quickbank
    bank = quickbank()
    makedoc(bank)
