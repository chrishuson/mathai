import time
import random
import os
import pickle


HOME = os.environ["HOME"]
dbdir = HOME + "/GitHub/mathai/db/"
outdir = HOME + "/GitHub/mathai/out/"

testflag = True
if testflag:
    dbdir = HOME + "/GitHub/mathai/test/db/"
    outdir = HOME + "/GitHub/mathai/test/out/"
    indir = HOME + "/GitHub/mathai/test/in/"

class ProblemSet():
	def __init__(self, problem_set_id=None, problems=None, spacing=None,
				problem_set_title=None, course_title=None, unit=None):
		""" Collection of problems that can be printed for assignment or discussion

			problem_set_id - int, key in problem_set_db
			problems - list, problem instances included in the problem set
			spacing - list, tex file layout information (e.g. newline location)
			problem_set_title - 3-tuple, header title str, date str, comment str
			course_title - str, title of the course e.g. 'Algebra 2'
			unit - str, chapter in the course the ProblemSet is applicable to
			"""
		
		self.problem_set_id = problem_set_id
		if problems is None:
			self.problems = []
		else:
			self.problems = problems
		self.spacing = spacing
		self.problem_set_title = problem_set_title
		self.course_title = course_title
		self.unit = unit

	def tex(self, title=None, texts_content_flags=None, meta=True, 
			numflag=True, head=None):
		""" Creates a worksheet LaTeX file that can be saved and rendered as pdf

	        title - 3-tuple, header title str, date str, comment str
				if absent, defaults to the problem_set title
	        text_content_flags - list, problem.tex options. Defaults to 'question'
			numflag - bool, number problems, i.e. prefix problems with "item"
			naked - bool, standalone problem tex, if True: wrap with head file
			head - str, LaTeX header to make problem.tex printable
			"""
		if title is None:
			title = self.problem_set_title
		problem_set_string = ''
		if head is None:
			try:
				with open(dbdir + 'head.tex', 'r') as f:
					head = f.read()
			except FileNotFoundError:
				print('Found no file head.tex in directory', dbdir)
				head = ''
		problem_set_string += head
		if title is not None:
			problem_set_string += '\n' + str(title[0]) + '\n'
		problem_set_string += r'\begin{enumerate}' + '\n'*2
		for problem in self.problems:
			problem_set_string += problem.tex(meta=meta, numflag=numflag) + '\n'
		problem_set_string += r'\end{enumerate}' + '\n' + r'\end{document}' + '\n'
		return problem_set_string


class LegacyProblemSet():
	def __init__(self, course_title, unit, topics = {}, problem_ids = {('last', 'first'): []}, \
					date = None, assessment = "incomplete"):
		""" Collection of problems that can be printed for assignment or discussion

			course_title - str, title of the course e.g. 'Algebra 2'
			unit - str, chapter in the course the ProblemSet is applicable to
			topics - dict of {topic: number of problems}
			problem_ids - dict of lists, problems by student {('last', 'first'):[prob_ids]}  --  TODO
			date - day/month/year
			average_class_skills - set default dict to become a dict of   -- TODO delete or implement
			{topic: average skill level for student in the respective course}
			in this __init__ method
			TODO the default values assigned as mutable objects leads to a problem, better =None, with and assignment within the init to and empty list or dictionary
			"""
		self.course_title = course_title
		self.unit = unit
		self.topics = topics
		self.problem_ids = problem_ids
		if self.topics == {'all': 'all'}: #?? I thought values were int number of problems
			self.problem_ids[('last', 'first')] = list(global_problem_dict['all']['all'].keys())
		elif problem_ids[('last', 'first')] == []: #TODO this risks throwing a KeyError if ('last', 'first') is not a student tuple
			self.problem_ids[('last', 'first')] = self.general_problem_ids()
		else:
			self.problem_ids = problem_ids
		self.date = date  # TODO convert to python date format

	def general_problem_ids(self, differentiated_students = []): #TODO change return to dict of lists (maybe)
		""" Return list of problem IDs 							# dict {problem_id: problem instance}

			Based on the average skill level of the class for each topic, generate a list of
			problem_ids for this ('last', 'first') problem set
			"""

		#ACCESS PROBLEMS ALREADY ASSIGNED TO STUDENTS
		past_problems = []
		for student_name in global_courses_dict[self.course_title].roster:
			if student_name not in differentiated_students:
				past_problems.extend(global_courses_dict[self.course_title].roster[student_name].problem_history.keys())

		#MAKE DICTIONARY W/ ALL TOPICS FOR A SPECIFIC CLASS POINTING TO THE AVERAGE SKILL LEVEL
		#FOR A STUDENT IN THAT CLASS
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

		#AFTER ACCESSING ALL AVAILABLE PROBLEMS FOR A CERTAIN TOPIC AND DIFFICULTY
		#REMOVE THE PROBLEMS ALREADY ASSIGNED TO STUDENTS AND GENERATE A RANDOM PROBLEM
		#FOR THE PSET FROM THE APPRROPRIATE UNUSED PROBLEMS
		problem_ids = []
		for topic in self.topics:
			students_skill = average_class_skills[topic]
			available_problems = global_problem_dict[topic][students_skill].keys()
			unused_problems =  set(available_problems) - set(past_problems)
			unused_problems_dict = {unused_problem:global_problem_dict[topic][students_skill][unused_problem]\
									for unused_problem in unused_problems}

			for _ in range(self.topics[topic]):
				problem_id = random.choice(unused_problems_dict.keys())
				problem_ids.append(problem_id)

		return problem_ids

	def tex(self, title, pflag=1, sflag=0, wflag=0, idflag=0, numflag=1):
	    """ Creates a worksheet LaTeX file

	        problem_ids: list of problem_ids to be included, in order
	        title: (out_filename, date, header)
	        #flags specify inclusion of problem text, solution & workspace
	        idflag: 2 print problem id (1: enhance for standards & meta info)
	        #numflag: 0 - no problem numbers; 1 prefix w "item" & includes "begin{enumerate}"
	        output file is out_filename.tex in the /out/ directory
	        """
	    outfile = outdir + title[0] + ".tex"

	    with open(outfile, "w") as newfile:
	        with open(dbdir + "head.tex", "r") as head:
	            for line in head:
	                newfile.write(line)
	        newfile.write(title[1] + r"\\*" + '\n' + r"\begin{center}{" + \
	                      title[2] + r"}\end{center}" + '\n')
	        if numflag == 1:
	            newfile.write(r'\begin{enumerate}' + '\n')

	        for pid in self.problem_ids[('last', 'first')]:
	            if numflag == 1:
	                newfile.write(r'\item ' + global_problem_dict["all"]["all"][pid].tex())
	            else:
	                newfile.write(global_problem_dict["all"]["all"][pid].tex().rstrip("\n")+r'\\*'+'\n')
	            if idflag == 1:
	                s = str(pid) + " " + global_problem_dict["all"]["all"][pid].tex(question = False, meta = True)
	                newfile.write(r'\\' + s + '\n')
	            elif idflag == 2:
	                newfile.write(r'\marginpar{' + str(pid) +r'}' + '\n')

	        if numflag == 1:
	            newfile.write(r'\end{enumerate}'+'\n')
	        with open(dbdir + "foot.tex", "r") as foot:
	            for line in foot:
	                newfile.write(line)


class DifferentiatedProblemSet(LegacyProblemSet):
	def __init__(self, course_title, unit, topics = {}, problem_ids = {('last', 'first'): []}, date = None, student_names = []):
		"""
			Inherited Attributes from ProblemSet class
				course_title - str, title of the course e.g. 'Algebra 2'
				unit - str, chapter in the course the ProblemSet is applicable to
				topics - dict of {topic: number of problems}
				problem_ids - dict of lists, problems by student {('last', 'first'):[problem_ids]})
				date - day/month/year
				average_class_skills - dict of {topic: average skill level
				for student in the respective course}
			student_names - list of student name tuples, (last, first)
			"""
		ProblemSet.__init__(self, course_title, unit, topics, date)

		if problem_ids[('last', 'first')] == []:
			self.problem_ids[('last', 'first')] = self.general_problem_ids() #I DECIDED TO SIMPLIFY TO AN ORDERED LIST OF IDS
		else:
			self.problem_ids = problem_ids

		self.student_names = student_names

		#generate differentiated problems for the students specified
		for student_name in self.student_names:
			self.problem_ids[student_name] = self.specific_problem_ids(student_name)

	def specific_problem_ids(self, student_name):
		#ACCESS PROBLEMS ALREADY ASSIGNED TO STUDENT
		student = global_students_dict[student_name]
		past_problems = global_courses_dict[self.course_title].roster[student_name].problem_history.keys()

		#AFTER ACCESSING ALL AVAILABLE PROBLEMS FOR A CERTAIN TOPIC AND DIFFICULTY
		#REMOVE THE PROBLEMS ALREADY ASSIGNED TO THE STUDENT AND GENERATE A RANDOM PROBLEM
		#FOR THE PSET FROM THE APPRROPRIATE UNUSED PROBLEMS
		problem_ids = []
		for topic in self.topics:
			students_skill = student.skillset[topic]
			available_problems = global_problem_dict[topic][students_skill].keys()
			unused_problems =  set(available_problems) - set(past_problems)
			unused_problems_dict = {unused_problem:global_problem_dict[topic][students_skill][unused_problem]\
									for unused_problem in unused_problems}

			for problem_number in range(self.topics[topic]):
				#build up to the hardest question
				question_difficulty = students_skill - problem_number + 1
				#make problem_bank global variable to be able to access here
				problem_id = random.choice(unused_problems_dict.keys())
				problem_ids.append(problem_id)
				#increment the difficulty of the next question
				question_difficulty += 1

		return problem_ids

def assign_problem_set(course_title, unit, topics, date = None, differentiated = False, specific_student_names = []):
	""" Returns a problem set instance, while also updating student problem and problem set histories

		course_title - str, title of the course e.g. 'Algebra 2'
		unit - str, chapter in the course the ProblemSet is applicable to
		topics - dict of {topic: number of problems}
		date - day/month/year
		differentiated - True/False specifying whether or not to generate only
						a general pset or differentiated ones for specific
						students as well
		specific_student_names - if differentiated, a list that details the
								students who should recieve a differentiated
								problem set
		"""
	problem_set = make_problem_set(course_title, unit, topics, date = None, differentiated = False, \
				specific_student_names = [])
	current_date = date
	
	#INITIAL CHECK TO SEE IF USER REQUESTED DIFFERENTIATED PSET FOR SOME STUDENT COHORT
	if differentiated:

		#ADJUST RESPECTIVE STUDENT'S PROBLEM SET AND PROBLEM HISTORY BASED ON DIFFERENTIATED PROBLEM
		#SET GENERATION
		for student_name in global_courses_dict[course_title].roster:
			if student_name in specific_student_names:
				global_students_dict[student_name].problem_set_history[current_date] = \
					(Assessment(problem_set.problem_ids[student_name], problem_set))
				global_students_dict[student_name].problem_history.update(problem_set.problem_ids[student_name])
			else:
				global_students_dict[student_name].problem_set_history[current_date] = \
					(Assessment(problem_set.problem_ids[('last', 'first')], problem_set))
				global_students_dict[student_name].problem_history.update(problem_set.problem_ids[('last', 'first')])

		return problem_set

	#ADJUST ALL STUDENTS' PROBLEM SET AND PROBLEM HISTORY BASED ON PROBLEM SET GENERATED
	for student in global_courses_dict[course_title].roster:
		global_students_dict[student].problem_set_history[current_date] = \
			(Assessment(problem_set.problem_ids[('last', 'first')], problem_set))
		global_students_dict[student].problem_history.update(problem_set.problem_ids[('last', 'first')])

	return problem_set

def make_problem_set(course_title, unit, topics, date = None, differentiated = False, \
				specific_student_names = []):
	""" Returns a problem set instance8

		course_title - str, title of the course e.g. 'Algebra 2'
		unit - str, chapter in the course the ProblemSet is applicable to
		topics - dict of {topic: number of problems}
		date - day/month/year
		differentiated - True/False specifying whether or not to generate only
						a general pset or differentiated ones for specific
						students as well
		specific_student_names - if differentiated, a list that details the
								students who should recieve a differentiated
								problem set

			"""
	if differentiated:
		return DifferentiatedProblemSet(course_title, unit, topics, date, {}, specific_student_names)

	return ProblemSet(course_title, unit, topics, date)


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
		return None


class Problem():
	def __init__(self, problem_id=None, topic='unassigned', \
				texts=None, standard=None, difficulty=3, \
				level=2, calc_type=1, source=None):
		""" Class for problem tex texts with attributes

			problem_id - int, key in problemdb
			topic - string describing problem topic e.g. logarithms
			texts - dict of relevant texts for a problem, keys: question,
				resource (graphs and images), workspace, instructions, answer,
				solution, rubric
			standard - ccss number, looked up if not an argument (TODO)
			difficulty: 1 - 10 (how hard it is)
			level: 1-6 (webworks /wiki/Problem_Levels) 2 simple steps,
					3 more complex algorithms, 5 word problems, 
					6 writing prompts
			calc_type: 0 no calculator allowed, 1 allowed, 2 calc practice
			source - string describing the author, or history of exercise e.g. "cjh"
			"""
		self.problem_id = problem_id
		self.topic = topic
		if texts is None:
			self.texts = {}
		else:
			self.texts = texts
		self.standard = standard
		try:
			self.difficulty = int(difficulty)
		except ValueError:
			print('difficulty must be 1-10')
		try:
			self.level = int(level)
		except ValueError:
			print('level must be 1-6')
		try:
			self.calc_type = int(calc_type)
		except ValueError:
			print('calc_type must be 0, 1, or 2')
		self.source = source
		self.meta = (str(self.problem_id) + ' ' #TODO static value is not right
				+ self.topic + ' ' + str(self.standard) + ' '
				+ str(self.difficulty) + ' ' + str(self.level) + ' '
				+ str(self.calc_type) + ' ' + str(self.source)
				)

	def tex(self, question=True, resource=False, workspace=False, \
					instructions=False, answer=False, solution=False, \
					rubric=False, meta=False, numflag=False, \
					naked=True, head=None):
		""" Returns the LaTeX to be included in a .tex file for printing

			flags - whether to include that field of texts information
			meta flag - whether to include the set of problem attributes
			numflag - bool, prefix with LaTeX "item" for numbering
			naked - bool, standalone problem tex, if True: wrap with head file
			head - str, LaTeX header to make problem.tex printable
			"""
		problem_string = ""
		if question:
			problem_string += self.texts.get("question")
		if resource:
			problem_string += self.texts.get("resource")
		if workspace:
			problem_string += self.texts.get("workspace")
		if instructions:
			problem_string += self.texts.get("instructions")
		if answer:
			problem_string += self.texts.get("answer")
		if solution:
			problem_string += self.texts.get("solution")
		if rubric:
			problem_string += self.texts.get("rubric")
		if meta:
			problem_string += '\n' + self.meta
		#newfile.write(r'\marginpar{' + str(id) +r'}' + '\n')
		if numflag:
			problem_string = r'\item ' + problem_string
		#print('Problem string is: ', problem_string)
		if not naked: #TODO with numflag==0 will lead to a LaTeX problem
			if head is None:
				head = self.make_tex_head()
				#print('\nhead is now: ', head)
			#return problem_string
			problem_string = (str(head) 
				+ r'\begin{enumerate}' + '\n'*2
				+ str(problem_string) + '\n'*2
				+ r'\end{enumerate}' + '\n'
				+ r'\end{document}' + '\n'
				)
		return problem_string

	def make_tex_head(self, title=None):
		""" Reads the head.tex file for the first lines of a tex file

			title - 3-tuple, str (worksheet sub heading, date, margin head)
			"""
		try:
			with open(dbdir + 'head.tex', 'r') as f:
				head = f.read()
		except FileNotFoundError:
				print('Found no file head.tex in directory', dbdir)
				head = ''
		if title is None:
			head += (r'\fancyhead[L]{BECA / Dr. Huson}' + '\n'*2 
					+ r'\begin{document}' + '\n'*2)
		else:
			head += (r'\fancyhead[L]{BECA / Dr. Huson / '
					+ title[2] + r'\\* ' + title[1] + r'}')
			head += '\n'*2 + r'\begin{document}' + '\n'*2
			head += r'\subsubsection*{' + title[0] + '}\n'
		return head
	"""
	def print_all(problem_id):
		print(problem_string)
		print(str(self.problem_id))
		print(self.topic)
		print(str(self.standard))
		print(str(self.difficulty))
		print(str(self.level))
		print(str(self.calc_type))
		print(str(self.source))
		"""


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
		for student in update_skills:
			self.roster[student].update_skillset(update_skills[student])

	def print_roster(self, skills_flag = 0):
		""" Prints out the student names in a class, optionally with topic skill levels

			"""
		for student in self.roster:
			print((self.roster[student].last_name, self.roster[student].first_name))
			if skills_flag:
				for topic in self.roster[student].skillset:
					print(topic, self.roster[student].skillset[topic])


class Student():
	def __init__(self, student_name_tuple, problem_history = {}, problem_set_history = {}, \
					skillset = {"Default": 3}):
		""" Student definition

			student_name_tuple - (last_name, first_name text strings)
			problem_history - dict of {problem_id: instance}
			problem_set_history - dict of {date: Assessment instance w/ problem_ids and
			assessment_status as attributes}
			skillset - dict of {topic:integer level of ability} from 0 to 10, topic = "Default"
			"""
		self.student_name = student_name_tuple
		self.first_name = student_name_tuple[1]
		self.last_name = student_name_tuple[0]
		self.problem_history = problem_history
		self.problem_set_history = problem_set_history
		self.skillset = skillset

	def update_skillset(self, update_skills):
		""" Function to update the student's skills

			update_skills - dict of {topic: current skill level +/- integer value}
			"""
		for topic in update_skills:
			self.skillset[topic] = self.skillset.get(topic, self.skillset["Default"])
			self.skillset[topic] += update_skills[topic]
			if self.skillset[topic] < 0:
				self.skillset[topic] = 0
			elif self.skillset[topic] > 10:
				self.skillset[topic] = 10

"""
p = dbdir + "global_courses_dict" + '.pickle'
with open(p, 'rb') as f:
	global_courses_dict = pickle.load(f)

p = dbdir + "global_students_dict" + '.pickle'
with open(p, 'rb') as f:
	global_students_dict = pickle.load(f)

p = dbdir + "global_problem_dict" + '.pickle'
with open(p, 'rb') as f:
	global_problem_dict = pickle.load(f)
"""
				