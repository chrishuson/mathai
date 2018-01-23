import random

class Worksheet():
	def __init__(self, student, topics, date):
		"""

			student - Student class instance
			topics - dict of {topic: number of problems}
			date - day/month/year
			"""
		self.student = student
		self.topics = topics
		self.date = date
		self.problem_ids = get_problem_ids()

	def get_problem_ids():
		#check here that a student's skill level in a topic corresponds to the
		#appropriate difficulty
		problem_ids = []
		for topic in self.topics:
			for problem_number in range(self.topics[topic]):
				student_skill = student.skillset[topic]
				#build up to the hardest question
				question_difficulty = student_skill - problem_number + 1
				#make problem_bank global variable to be able to access here
				problem_ids.append(random.sample(problem_bank[topic][question_difficulty]), 1)
				#increment the difficulty of the next question
				question_difficulty += 1

		return problem_ids





class Problem():
	def __init__(self, topic, standard, calc_type, difficulty, level, text_inputs, text_flags, source):
		""" A problem instance contains the followign specific attributes

			topic - string describing problem topic e.g. logarithms
			standard - 
			calc_type: 0 no calculator allowed, 1 allowed, 2 calc practice
			difficulty: 1 - 10
			level: 1-6 (webworks reference)
			text_inputs - list of relevant texts for a problem, e.g. problem text, workspace
						  text, solution text, reference text, etc.
			text_flags - list of True/False that correspond to the text_inputs and whether or
						 to in include the relevant input on the worksheet e.g.
						 text_inputs = [problem_text, solution_text]
						 text_flags = [True, False] indicates to include the problem_text, but
						 not the solution_text on the worksheet
			source - string describing the author, or history of exercise e.g. "cjh"
			"""
		self.topic = topic
		self.standard = standard
		self.calc_type = calc_type
		self.difficulty = difficulty
		self.level = level
		self.text_inputs = text_inputs
		self.text_flags = text_flags
		self.source = source


#Initially load and update these files using pickle
def make_worksheet(course_title):
	#initial attempt at a make worksheet function to organize the various updates and storage
	#that need to occur
	for student in courses[course_title]:


def initial_problem_bank_creation(problem_list):
	problem_bank = {}
	#Make initial problem bank here depending on the format of problem list w/ following
	#data structure {Topic: {difficulty: {id: instance}}}

	return problem_bank

def add_problem():
	#add problem here to problem bank in same format

def inital_courses_creation(courses_dict):
	#courses = {id: course_instance, ...}

def add_course():

def initial_student_creation(students):

def add_student():

class Course():
	def __init__(self, title, roster):
		""" Courses contain students and are used to make worksheet assignments

			roster - list of name strings
			"""
		self.course_title = title
		self.roster = {}
		for student in roster:
			self.roster[student.name] = student

		def update_student_skills(self, update_skills):
			""" Function to update the students within a course based on improved/worsened abilites

				update_skills - dict of {student: {skill: current skill level +/- integer value}}
				"""
			for student in update_skills:
				updated_student = self.roster[student].update_skillset(update_skills[student])
				self.roster[student] = updated_student

class Student():
	def __init__(self, name, skillset = None):
		""" Student definition

			name - single text string
			skillset - dict of {topic:integer level of ability}, level of ability from 0 to 10
			"""
		self.name = name
		#still need to specify what default skillset would be
		default_skillset = {}

		#make sure a skillset has been specified, or make it the default if not
		if skillset == None:
			self.skillset = default_skillset
		else:
			self.skillset = skillset

	def update_skillset(self, update_skills):
		""" Function to update the student's skills

			update_skills - dict of {skill: current skill level +/- integer value}
			"""
		for skill in update_skills:
			self.skillset[skill] += update_skills[skill]


# Temporary testing section
names = ["Elias", "Marcus"]
skillset = {"Inverse of Functions":3, "Evaluating Expressions":2, \
			"Evaluating Logarithmic Expressions":5}
cIB1 = Course(names, skillset)
for s in cIB1.student_instances:
	print(s.name, s.skillset["Inverse of Functions"])
