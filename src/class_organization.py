import time
import random


#ADDS STUDENT TO GLOBAL STUDENTS DICTIONARY IN APPROPRIATE FORM
def add_student(student_name_tuple):
	""" Arg (last name text:, first name text)

		Creates new instance of a student and adds entry to global students dict
		"""
	global_students_dict[student_name_tuple] = Student(student_name_tuple)


#ADDS COURSE TO GLOBAL COURSES DICTIONARY IN APPROPRIATE FORM
def add_course(title, students):
	global_courses_dict[title] = Course(title, students)


def add_problem(topic, difficulty = 3):
	#SOMETHING HERE (PERHAPS THE __INIT__ FUNCTION SHOULD RECORD PROBLEM IN GLOBAL DICT)
	return

class ProblemSet():
	def __init__(self, topics, date, course_title, assessment = "incomplete"):
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

		#TO DO - MAKE PROBLEM_IDS INTO DICT OF {'GENERAL': {ID: INSTANCE}}
		self.problem_ids = {'general': self.general_problem_ids(students)}

	def general_problem_ids(self, differentiated_students = []):
		"""
		Based on the average skill level of the class for each topic, generate a list of
		problem_ids for this 'general' problem set

			"""
		past_problems = []
		for student_name in global_courses_dict[self.course_title].roster and not in differentiated_students:
			past_problems.extend(global_courses_dict[self.course_title].roster[student_name].problem_history.keys())

		average_class_skills = {}
		for topic in self.topics:
			#initialize both topic_score and student_count at 0
			topic_score = 0
			student_count = 0
			#access each student's Student class instance from the course's roster
			#to add their topic skill level to the topic_score
			for student_name in global_courses_dict[self.course_title].roster:
				if student_name not in differentiated_students:
					topic_score += global_courses_dict[self.course_title].roster[student_name].skillset[topic]
					student_count += 1
			average_class_skills[topic] = round(topic_score/student_count)

		problem_ids = {}
		for topic in self.topics:
			students_skill = average_class_skills[topic]
			available_problems = global_problem_dict[topic][students_skill].keys()
			unused_problems =  set(available_problems) - set(past_problems)
			unused_problems_dict = {unused_problem:global_problem_dict[topic][students_skill][unused_problem]\
									for unused_problem in unused_problems}

			for problem_number in range(self.topics[topic]):
				problem_id = random.choice(unused_problems_dict.keys())
				problem_ids[problem_id] = unused_problems_dict[problem_id]

		return problem_ids

class DifferentiatedProblemSet(ProblemSet):
	def __init__(self, topics, date, course_title, student_names):
		"""
			Inherited Attributes from ProblemSet class
				topics - dict of {topic: number of problems}
				date - day/month/year
				course_title - title of the course as str, e.g. 'Algebra 2'
				average_class_skills - dict of {topic: average skill level
				for student in the respective course}

			student_names - list of student name tuples, (last, first)
			"""
		ProblemSet.__init__(self, topics, date, course_title)
		self.problem_ids = {'general': self.general_problem_ids([name for name in student_names])}
		# problem_ids IS DICT {STUDENT TUPLE: [PROBLEM IDs]}
		self.student_names = student_names

		#generate differentiated problems for the students specified
		for student_name in self.student_names:
			self.problem_ids[student_name] = self.specific_problem_ids(student_name)

	def specific_problem_ids(self, student_name):
		#access student instance of student names to base problem selections off student skillset
		student = global_students_dict[student_name]
		past_problems = global_courses_dict[self.course_title].roster[student_name].problem_history.keys()

		problem_ids = {}
		for topic in self.topics:
			students_skill = student.skillset[topic]
			available_problems = global_problem_dict[topic][students_skill].keys()
			unused_problems =  set(available_problems) - set(past_problems)		
			unused_problems_dict = {unused_problem:global_problem_dict[topic][students_skill][unused_problem]\
									for unused_problem in unused_problems}

			for problem_number in range(self.topics[topic]):
				#build up to the hardest question
				question_difficulty = student_skill - problem_number + 1
				#make problem_bank global variable to be able to access here
				problem_id = random.choice(unused_problems_dict.keys())
				problem_ids[problem_id] = unused_problems_dict[problem_id]
				#increment the difficulty of the next question
				question_difficulty += 1

		return problem_ids

def make_problem_set(course_title, topics, date, differentiated = False, specific_student_names = []):
	""" 
		

		"""
	current_date = time.strftime("%d/%m/%Y")
	if differentiated:
		diff_problem_set = DifferentiatedProblemSet(topics, date, course_title, {}, specific_student_names)
		for student_name in global_courses_dict[course_title].roster:
			if student_name in specific_student_names:
				global_students_dict[student_name].problem_set_history[current_date] = \
					(Assessment(diff_problem_set.problem_ids[student_name], diff_problem_set))
				global_students_dict[student_name].problem_history.update(diff_problem_set.problem_ids[student_name])
			else:
				global_students_dict[student_name].problem_set_history[current_date] = \
					(Assessment(diff_problem_set.problem_ids['general'], diff_problem_set))	
				global_students_dict[student_name].problem_history.update(diff_problem_set.problem_ids['general'])

		return diff_problem_set

	problem_set = ProblemSet(topics, date, course_title)
	for student_name in global_courses_dict[course_title].roster:
		global_students_dict[student_name].problem_set_history[current_date] = \
			(Assessment(problem_set.problem_ids['general'], problem_set))	
		global_students_dict[student_name].problem_history.update(problem_set.problem_ids['general'])

	return problem_set


class Assessment():
	def __init__(self, problem_ids, problem_set, assessment_status = "incomplete"):
		""" An Assessent instance contains the following specific attributes

			assessment_status - either str describing incomplete/complete status or dict
								possibly indicating student score for specific problems

			"""
		self.problem_ids = problem_ids
		self.problem_set = problem_set
		self.assessment_status = assessment_status

	#FIGURE OUT HOW TO DO THIS
	def update_assessment(self):
		return


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
	def __init__(self, title, students):
		""" Courses contain students and are used to make worksheet assignments

			title - str description of course title
			students - dict of {(last name, first name): Student instance}
			"""
		self.course_title = title
		self.roster = students

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
	def __init__(self, student_name_tuple, problem_set_history = {}, \
					skillset = None, in_global_dict = True):
		""" Student definition

			(last_name, first_name text strings)
			problem_set_history - dict of {date: Assessment instance w/ problem_ids and
			assessment_status as attributes}
			skillset - dict of {topic:integer level of ability} from 0 to 10
			"""
		self.student_name = student_name_tuple
		self.first_name = student_name_tuple[1]
		self.last_name = student_name_tuple[0]
				self.problem_history = problem_history
		self.problem_set_history = problem_set_history
		if in_global_dict:
			global global_students_dict
			global_students_dict[student_name_tuple] = self
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
