# Functions to list files and crawl directories for problem set files

import os

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




