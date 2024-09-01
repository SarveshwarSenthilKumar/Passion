import sqlite3
import os

os.remove("users.db")
connection = sqlite3.connect("users.db")
crsr = connection.cursor()
crsr.execute("CREATE TABLE users (id INTEGER, username TEXT NOT NULL,  password TEXT NOT NULL, rank, PRIMARY KEY(id))")
connection.commit()
crsr.close()
connection.close()
test = open("users.db", "r")
test.close()