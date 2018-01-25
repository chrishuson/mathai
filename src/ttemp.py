import pickle

#Hydrogen path config workaround:
#%cd src
%pwd

from main import loaddbfile
from class_organization import ProblemSet, Problem, Course, Student

#ct = loaddbfile("courses")

# Temporary sandbox lines of code are below
roster = ["Elias", "Marcus"]
skillset = {"Inverse of Functions":3, "Evaluating Expressions":2, \
			"Evaluating Logarithmic Expressions":5}
cIB1 = Course("11.1 IB Math SL", roster)

for student in cIB1.roster:
	cIB1.roster[student].skillset = skillset

cIB1.print_roster(1) #not sure why this doesn't work.

question = "What is the equation of a line parallel to $y=-3x+6$ with a $y$-intercept of 5?"
texts = {"question":question}
topic = "Writing Linear Equations"

p1 = Problem(topic, texts)

print(p1.format(1))
print(p1.texts["question"])
