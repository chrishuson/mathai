# Functions to list files and crawl directories for problem set files


"""
Notes 
short_df['fullfilename'] = course_dir + '/' + short_df.unit + '/' + short_df.filename

short_df['text_tuple'] = short_df.fullfilename.apply(parse_tex_file)

short_df[['packages', 'header', 'body']] = pd.DataFrame(short_df.text_tuple.tolist(), index=short_df.index)

short_df[['problems', 'spacing']] = pd.DataFrame(short_df.problem_tuple.tolist(), index=short_df.index)

for unit in course_files:
    print(unit, len(course_files[unit]))

print(set(course_frame['unit']))
print(course_frame[course_frame['unit'].isin(['Misc'])])

course_frame.to_csv('crawler_course_frame.csv') # ,index=False to avoid saving
new = pd.read_csv('crawler_course_frame.csv')

worksheet_path = dbdir + '/' + 'worksheet_files_df.csv' #better os.path.join(list)
worksheet_files_df = pd.read_csv(worksheet_path)
worksheet_files_df.tail(10)

filename = 'problems_df'
problems_df.to_csv(os.path.join(dbdir, filename+'.csv'))
short_problems_df = pd.read_csv(os.path.join(dbdir, 'short_problems_df.csv'))



To combine problem question text from a dataframe, first make list into string:
    lines = ps_df.agg(lambda x: ''.join(x))
        then join into a long string for printing
    out = lines.str.cat(sep=r'\n') , or also line = 'abc'.join(lines)

pass unit and filename to parse_tex_file:
filenames = os.path.join([course_dir, worksheet_files_df.unit, worksheet_files_df.filename])
    """