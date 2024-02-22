import sqlite3

connection = sqlite3.connect('db/rendezvous.db')
cursor = connection.cursor()

with open('db/rendezvous.sql', 'r') as sql_file:
    sql_script = sql_file.read()

cursor.executescript(sql_script)

connection.commit()
connection.close()
