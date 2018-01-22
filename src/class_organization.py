class Worksheet():
	def __init__(self, some_course, topics, data_source, problem_bank):
		"""
		some_course (class instance): details the relevant course to generate worksheets for
		topics (dict): {problem_type e.g. logs, vectors, etc. : (number of mc problems
		of that type, number of word problems of that type)}
		data_source
		"""
		self.some_course = some_course
		self.topics = topics
		self.data_source = data_source
		self.problem_bank = problem_bank
		self.worksheets = []
		for student in some_course:
			self.worksheets.append(generate_worksheet(student))

	def generate_worksheet(self, student):
		student_worksheet = []

		# add a problem to a worksheet if the topics, problem_type,
		# necessary skills of the student, and data_source match up with
		# the specifications initialized
		for topic in topics:
			mc_probs = 0
			word_probs = 0

			while mc_probs <= self.topics[topic][0]:
				for problem in problem_bank[topic]:
					#if all specifications are met:
						#student_worksheet.append(problem)
						#mc_probs += 0

			while word_probs <= topics[topic][1]:
				for problem in problem_bank[topic]:
					#if all specifications are met:
						#student_worksheet.append(problem)
						#word_probs += 0

		return student_worksheet

	def make_pdf(self):
		for worksheet in self.worksheets:
			#make pdf of worksheet data

#make a dict of problem instances with key being the problem topic and
#value being the set of all problems that cover that topic
#Example {'logs': {PROBLEM SET HERE w/ instances of Problem class},
#'vectors': {PROBLEM SET HERE w/ instances of Problem class}}


class Problem():
	def __init__(self, mc = False, word = False, student, necessary_skills, problem_topic, data_source)
		self.mc = mc
		self.word = word
		self.student = student
		self.necessary_skills = necessary_skills
		self.problem_topic = problem_topic
		self.data_source = data_source

	def check_compatibility(self):
		#check compatability here for specifications above
		for skill1 in self.necessary_skills:
			if self.necessary_skills[skill1] < self.student.skillset[skill1] or self.necessary_skills[skill1] > self.student.skillset[skill1] + 1:
				return False

		return True

class Course():
	def __init__(self, students, skillset):
		""" Courses contain students and are used to make worksheet assignments

			students - list of name strings
			skillset - dict of {topic:integer value}
			"""
		self.student_instances = self.make_student_instances(students, skillset)
		self.students_skills = {}
		for student in self.student_instances:
			self.students_skills[student.name] = student.skillset

	def make_student_instances(self, student_names, skillset):
		student_instances = []
		for student in student_names:
			student_instances.append(Student(student, skillset))

		return student_instances

class Student():
	def __init__(self, name, skillset):
		""" Student definition

			name - single text string
			skillset - dict of {topic:integer level of ability}
			"""
		self.name = name
		self.skillset = skillset

	def update_student_skills(self, skills, correct = True):
		for skill in skills:
			if correct:
				self.skillset[skill] += 1
			else:
				self.skillset[skill] -= 1

# Temporary testing section
names = ["Elias", "Marcus"]
skillset = {"Inverse of Functions":3, "Evaluating Expressions":2, \
			"Evaluating Logarithmic Expressions":5}
cIB1 = Course(names, skillset)
for s in cIB1.student_instances:
	print(s.name, s.skillset["Inverse of Functions"])

#how to do this
def post_worksheet_course_update(some_course):

#initial input with skills update
def initial_problem_bank(data_source):
