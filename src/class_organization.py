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
	def __init__(self, topic, texts, standard = None, calc_type = 1, \
					difficulty = 3, level = 2, source = None):
		""" A problem instance contains the followign specific attributes

			topic - string describing problem topic e.g. logarithms
			texts - dict of relevant texts for a problem, keys: question,
				resource (graphs and images), workspace, answer, solution, rubric
			standard - ccss number, looked up if not an argument
			calc_type: 0 no calculator allowed, 1 allowed, 2 calc practice
			difficulty: 1 - 10 (how hard it is)
			level: 1-6 (webworks /wiki/Problem_Levels) 2 simple steps,
					3 more complex algorithms, 5 word problems, 6 writing prompts
			source - string describing the author, or history of exercise e.g. "cjh"
			"""
		self.topic = topic
		self.standard = standard
		self.calc_type = calc_type
		self.difficulty = difficulty
		self.level = level
		self.texts = texts
		self.source = source

	def format(self, text_flags):
		""" Returns the LaTeX to be included in a .tex file for printing

			text_flags - list of True/False that correspond to the text_inputs and whether or
						 to in include the relevant input on the worksheet e.g.
						 text_inputs = [problem_text, solution_text]
						 text_flags = [True, False] indicates to include the problem_text, but
						 not the solution_text on the worksheet
			"""
		problem_string = ""
		if True:
			problem_string += self.texts["question"]
		return problem_string



#Initially load and update these files using pickle
def make_worksheet(course_title):
	#initial attempt at a make worksheet function to organize the various updates and storage
	#that need to occur
	worksheet_list = []
	# Would the result be a list of worksheet instances, one for each student?
	for student in courses[course_title]:
		ps = Worksheet(student, topics, date)
		worksheet_list.append(ps)
	return worksheet

def initial_problem_bank_creation(problem_list):
	""" Doc string

		"""
	problem_bank = {}
	#Make initial problem bank here depending on the format of problem list w/ following
	#data structure {Topic: {difficulty: {id: instance}}}

	return problem_bank

def add_problem():
	#add problem here to problem bank in same format
	return_object = [] # This is a dummy line so python doesn't complain on import

def inital_courses_creation(courses_dict):
	#courses = {id: course_instance, ...}
	return_object = []

def add_course():
	return_object = []

def initial_student_creation(students):
	return_object = []

def add_student():
	return_object = []

class Course():
	def __init__(self, title, names):
		""" Courses contain students and are used to make worksheet assignments

			names - list of student name strings
			Might we want to add an optional arg default_skillset = None ?
			"""
		self.course_title = title
		self.roster = {}
		for name in names: # Perhaps we should use "name" instead of "student" in these two lines
			self.roster[name] = Student(name)
			# Might be confusing that we init with a roster = list, but return self.roster is a dict
			# Is self.roster a dict of {text name: student instance}

		def update_student_skills(self, update_skills):
			""" Function to update the students within a course based on improved/worsened abilites

				update_skills - dict of {student: {skill: current skill level +/- integer value}}
				"""
			for student in update_skills:
				updated_student = self.roster[student].update_skillset(update_skills[student])
				self.roster[student] = updated_student

		def print_roster(self, skills_flag = 0):
			""" Prints out the student names in a class, optionally with topic skill levels

				"""
			for student in self.roster:
				print(self.roster[student].name)
				print(skills_flag)
				if skills_flag:
					for topic in self.roster[student].skillset:
						print(topic, self.roster[student].skillset[topic])

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
