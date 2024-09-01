import sqlite3
from sql import *
import os
from datetime import datetime
import pytz

os.remove("dj.db")
connection = sqlite3.connect("dj.db")
crsr = connection.cursor()
crsr.execute("CREATE TABLE dj (id INTEGER, name TEXT NOT NULL, time, PRIMARY KEY(id))")

tz_NY = pytz.timezone('America/New_York')
now=datetime.now(tz_NY)
OTime= now.strftime("%d/%m/%y %H:%M:%S")

db = SQL("sqlite:///dj.db")
db.execute("INSERT INTO dj (name, time) VALUES(?,?)", "No DJ Yet", OTime)

connection.commit()
crsr.close()
connection.close()
test = open("dj.db", "r")
test.close()