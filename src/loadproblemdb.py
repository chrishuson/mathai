import sqlite3
conn = sqlite3.connect('mathai.db')

c = conn.cursor()

# Create table for problem
#c.execute('''CREATE TABLE problems
#            (skill text, short text, long text, solution text, instruction text, hint text)''')

# Insert problem
c.execute("""INSERT INTO problems VALUES (
          'exponents', 'negative whole numbers',
          '\item $15x^{2}y^2 \div 3x^5 y^{2}$',
          '$\frac{5}{x^3}$', 'Simplify with no negative exponents',
          'Negative exponents mean denominator')""")

# Save
conn.commit()
conn.close()
