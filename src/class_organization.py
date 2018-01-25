#THESE INITIAL GLOBAL CREATIONS DEPEND ON HOW THE DATA IS ORGANIZED FOR INPUT
#GLOBAL CREATION OF STUDENTS DICTIONARY {FULL STUDENT NAME: STUDENT INSTANCE}
global_students_dict = {}
for student_name in student_data_list:
	add_student(student_name)

#ADDS STUDENT TO GLOBAL STUDENTS DICTIONARY IN APPROPRIATE FORM
def add_student(student_name):
	first_and_last_name = student_name.split(' ')
	global_students_dict[(first_and_last_name[1], first_and_last_name[0])] = \
	Student(first_and_last_name[1], first_and_last_name[0])


#GLOBAL CREATION OF COURSES DICTIONARY {COURSE TITLE: COURSE INSTANCE}
global_courses_dict = {}
for course_title in courses_data_dict:
	add_course(course_title, courses_data_dict[course])

#ADDS COURSE TO GLOBAL COURSES DICTIONARY IN APPROPRIATE FORM
def add_course(title, names):
	global_courses_dict[title] = Course(title, names)


#GLOBAL CREATION OF PROBLEM BANK DICTIONARY {TOPIC: {DIFFICULTY: {ID: INSTANCE}}}

global_problem_dict = {}
for problem in problem_data_dict:
	add_problem()

def add_problem():
	#SOMETHING HERE
	return
class ProblemSet():
	def __init__(self, topics, date, course_title, average_class_skills = {}):
		"""
			topics - dict of {topic: number of problems}
			date - day/month/year
			course_title - title of the course as str, e.g. 'Algebra 2'
			average_class_skills - set default dict to become a dict of
			{topic: average skill level for student in the respective course}
			in this __init__ method

			"""
		self.topics = topics
		self.date = date
		self.course_title = course_title
		self.problem_ids = {'general': self.general_problem_ids(students)}
		self.average_class_skills = average_class_skills
		for topic in self.topics:
			#initialize both topic_score and student_count at 0
			topic_score = 0
			student_count = 0
			#access each student's Student class instance from the course's roster
			#to add their topic skill level to the topic_score
			for student_name in global_courses_dict[self.course_title].roster:
				topic_score += global_courses_dict[self.course_title].roster[student_name].skillset[topic]
				student_count += 1
			self.average_class_skills[topic] = round(topic_score/student_count)

	def general_problem_ids(self):
		"""
		Based on the average skill level of the class for each topic, generate a list of
		problem_ids for this 'general' problem set

			"""
		problem_ids = []
		for topic in self.topics:
			students_skill = self.average_class_skills[topic]
			for problem_number in range(self.topics[topic]):
				problem_ids.append(random.sample(global_problem_dict[topic][students_skill]), 1)

		return problem_ids

class DifferentiatedProblemSet(ProblemSet):
	def __init__(self, topics, date, course_title, average_class_skills, student_names):
		"""
			Inherited Attributes from ProblemSet class
				topics - dict of {topic: number of problems}
				date - day/month/year
				course_title - title of the course as str, e.g. 'Algebra 2'
				average_class_skills - dict of {topic: average skill level
				for student in the respective course}

			student_names - list of student name tuples, (last, first)
			"""
		ProblemSet.__init__(self, topics, date, course_title, average_class_skills)
		self.problem_ids = {'general': [self.general_problem_ids()]}
		self.student_names = student_names

		#generate differentiated problems for the students specified
		for student_name in self.student_names:
			self.problem_ids[student_name] = [self.specific_problem_ids(student_name)]

	def specific_problem_ids(self, student_name):
		#access student instance of student names to base problem selections off student skillset
		student = global_students_dict[student_name]
		problem_ids = []
		for topic in self.topics:
			for problem_number in range(self.topics[topic]):
				student_skill = student.skillset[topic]
				#build up to the hardest question
				question_difficulty = student_skill - problem_number + 1
				#make problem_bank global variable to be able to access here
				problem_ids.append(random.sample(global_problem_dict[topic][question_difficulty]), 1)
				#increment the difficulty of the next question
				question_difficulty += 1

		return problem_ids

def make_problem_set(course_title, topics, date, differentiated = False, specific_student_names = []):
	#create an instance of the appropriate class depending on user specifications
	if differentiated:
		return DifferentiatedProblemSet(topics, date, course_title, {}, specific_student_names)
	return ProblemSet(topics, date, course_title)

class Problem():
	def __init__(self, topic, texts, standard = None, calc_type = 1, \
					difficulty = 3, level = 2, source = None):
		""" A problem instance contains the following specific attributes

			topic - string describing problem topic e.g. logarithms
			texts - dict of relevant texts for a problem, keys: question,
				resource (graphs and images), workspace, instructions, answer,
				solution, rubric
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

class Course():
	def __init__(self, title, names):
		""" Courses contain students and are used to make worksheet assignments

			names - list of student name strings
			Might we want to add an optional arg default_skillset = None ?
			"""
		self.course_title = title
		self.roster = {}
		for name in names:
			first_and_last_name = name.split(' ')
			self.roster[(first_and_last_name[1], first_and_last_name[0])] = \
			Student(first_and_last_name[1], first_and_last_name[0])
			# Might be confusing that we init with a roster = list, but return self.roster is a dict
			# Is self.roster a dict of {text name: student instance}

		def update_student_skills(self, update_skills):
			""" Function to update the students within a course based on improved/worsened abilites

				update_skills - dict of {(student last name, student first name):
				{skill: current skill level +/- integer value}}
				"""
			for student_name in update_skills:
				self.roster[student_name].update_skillset(update_skills[student_name])

		def print_roster(self, skills_flag = 0):
			""" Prints out the student names in a class, optionally with topic skill levels

				"""
			for student_name in self.roster:
				print((self.roster[student_name].last_name, self.roster[student_name].first_name))
				print(skills_flag)
				if skills_flag:
					for topic in self.roster[student].skillset:
						print(topic, self.roster[student].skillset[topic])

class Student():
	def __init__(self, first_name, last_name, problem_set_history = [], course_history = [], skillset = None):
		""" Student definition

			first_name - single text string
			last_name - single text string
			problem_set_history -
			course_history -
			skillset - dict of {topic:integer level of ability}, level of ability from 0 to 10
			"""
		self.first_name = first_name
		self.last_name = last_name
		self.problem_set_history = []
		self.course_history = []
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
