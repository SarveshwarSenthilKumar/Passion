import sqlite3
import os

os.remove("links.db")
connection = sqlite3.connect("links.db")
crsr = connection.cursor()
crsr.execute("CREATE TABLE links (id INTEGER, description, name, link, PRIMARY KEY(id))")
connection.commit()
crsr.close()
connection.close()
test = open("links.db", "r")
test.close()