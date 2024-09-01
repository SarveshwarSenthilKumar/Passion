import sqlite3
import os

os.remove("bb.db")
connection = sqlite3.connect("bb.db")
crsr = connection.cursor()
crsr.execute("CREATE TABLE bb (id INTEGER, name TEXT NOT NULL, guess, time, PRIMARY KEY(id))")
connection.commit()
crsr.close()
connection.close()
test = open("bb.db", "r")
test.close()