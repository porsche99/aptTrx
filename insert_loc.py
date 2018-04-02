import re
import sqlite3

conn = sqlite3.connect('../loc.db')
c = conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS location(loc text PRIMARY KEY, code text)')
conn.commit()

f = open('loc.txt')

for d in f.readlines():
    data = re.sub(r'\s{2}', '|', d.strip()).split('|')
    print(data[1].strip(), data[0])
    c.execute('INSERT or REPLACE INTO location VALUES ("%s", "%s")'%(data[1].strip(), data[0]))

c.execute('SELECT * FROM location')
locData = c.fetchall()
print(locData)

conn.commit()
f.close()
