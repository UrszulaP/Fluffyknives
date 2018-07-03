import sqlite3

conn = sqlite3.connect('database.db')
c = conn.cursor()

with open('db_scheme.sql', 'r', encoding='utf-8') as file:
	create_db = file.read()

c.executescript(create_db)

conn.commit()
conn.close()
