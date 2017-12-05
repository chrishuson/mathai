#makes tex document
#input files are fixed '.tex' head, title, and foot
#and problem containing a list of \item lines
def makeset(n):
    """n is the number of problem lines returned in a list"""
    problems = open("mathai/tex/problems.tex", "r")
    problemlist = []
    problempick = []
    for line in problems:
        problemlist.append(line)
    for i in range(n):
        problempick.append(problemlist[i])
    return problempick


newfile = open("mathai/tex/newfile.tex", "w")
head = open("mathai/tex/head.tex", "r")
for line in head:
    newfile.write(line)

title = open("mathai/tex/title.tex", "r")
for line in title:
    newfile.write(line)

#problem section to begin and end with enumerate
newfile.write(r'\begin{enumerate}'+'\n')
problemset = makeset(3)
for i in range(3):
    newfile.write(problemset[i])

newfile.write(r'\end{enumerate}'+'\n')

foot = open("mathai/tex/foot.tex", "r")
for line in foot:
    newfile.write(line)
newfile.close()
