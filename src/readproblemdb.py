import sqlite3
conn = sqlite3.connect('mathai.db')

c = conn.cursor()

for row in c.execute('SELECT * FROM problems'):
    print(row)
    
