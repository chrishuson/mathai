# Functions to list files and crawl directories for problem set files

import os

import numpy as np
import pandas as pd


HOME = os.environ["HOME"]
cwd = os.getcwd()

print('Current Working Directory is: ', cwd)
print('Home is: ', HOME, '\n')

os.chdir('/Users/chris/GitHub/course-files/Geometry')

#use scandir instead of listdir
unit_directories = []
with os.scandir() as d:
    for unit in d:
        if not unit.name.startswith('.') and unit.is_dir():
            unit_directories.append(unit.name)

unit_directories.sort()

course_files = {}
for unit in unit_directories:
    unit_texfiles = []
    with os.scandir(unit) as d:
        for entry in d:
            if entry.name.endswith('.tex'):
                unit_texfiles.append(entry.name)
    course_files[unit] = unit_texfiles

for unit in course_files:
    print(unit, len(course_files[unit]))

file_list = []
for unit in course_files:
    length = len(course_files[unit])
    for worksheet in course_files[unit]:
        file_list.append((unit, length, worksheet))

course_frame = pd.DataFrame(file_list)
column_names = ['unit', 'worksheet_count', 'worksheet_file_name']
course_frame.columns = column_names

print(set(course_frame['unit']))
print(course_frame[course_frame['unit'].isin(['Misc'])])

course_frame.to_csv('crawler_course_frame.csv')
new = pd.read_csv('crawler_course_frame.csv')