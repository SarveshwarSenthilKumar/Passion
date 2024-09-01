
#By Sarveshwar Senthilkumar in 2021

from flask import Flask, render_template, request, redirect, session
from flask_session import Session 
import os
import sqlite3
from datetime import datetime
from datetime import timedelta
import random
import pytz
import shutil
from sql import *
from collections import defaultdict
from collections import Counter

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = True
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/addquestion", methods=["GET", "POST"])
def addaquastion():
  if not session.get("name"):
    return redirect("/")
  question = request.form.get("question")
  minimum = int(request.form.get("min"))
  maximum = int(request.form.get("max"))

  file = open("question.txt", "w")
  file.write(question+"\n")
  stringMM = str(minimum) + " " + str(maximum)
  file.write(stringMM)
  file.close()

  return redirect("/t")

@app.route("/deleteflask")
def deleteflask():
  if not session.get("name") or session.get("rank") == "2":
    return redirect("/")
  shutil.rmtree("flask_session")
  app.config["SESSION_PERMANENT"] = True
  app.config["SESSION_TYPE"] = "filesystem"
  Session(app)
  
  return redirect("/")


@app.route("/previousdj")
def previousdjs():
  results=[]
  for i in open("djs.txt", "r"):
    results.append(i.strip())
  return render_template("prevDJ.html", results=results, type="dj")

@app.route("/releasenotes")
def releasenotes():
  results=[]
  for i in open("releaseNotes.txt", "r"):
    results.append(i.strip())
  return render_template("prevDJ.html", results=results, type="releaseNotes")

@app.route("/deltlink", methods=["GET","POST"])
def deletlink():
  if not session.get("name") or session.get("rank") == "2":
    return redirect("/")
  else:
    id=request.args.get("data")

    db = SQL("sqlite:///links.db")
    db.execute("DELETE FROM links WHERE id = :id", id=id)

    test = open("links.db", "a")
    test.write("")
    test.close()

    return redirect("/t")

@app.route("/ss")
def ss():
  db = SQL("sqlite:///bb.db")
  db.execute("DELETE FROM bb WHERE name = :name", name="Sarv")

  return redirect("/random")

@app.route("/deltacc", methods=["GET","POST"])
def deletacc():
  if not session.get("name") or session.get("rank") == "2":
    return redirect("/")
  else:
    id=request.args.get("data")

    db = SQL("sqlite:///users.db")
    db.execute("DELETE FROM users WHERE username = :id", id=id)

    test = open("users.db", "a")
    test.write("")
    test.close()

    return redirect("/t")

@app.route("/querydata")
def querydata():
  
  queries = defaultdict(int)
  totalsearches=0
  totalsearchlength=0
  for i in open("queries.txt", "r"):
      i=i.lower()
      i = i.replace(" ","_")
      queries[i]+=1
      totalsearches+=1
      totalsearchlength+=len(i)

  keys=[]
  values=[]
  k = Counter(queries)

  queries = k.most_common(10)
  queries=queries[::-1]

  topsearches=0

  for key, value in queries:
    key=key[:-1]
    keys.append(key)
    values.append(value)

  keys=keys[:10]
  values=values[:10]
  strkeys=""
  for i in keys:
    strkeys += i + " , "
  strvalues=""
  for i in values:
    strvalues += str(i) + " , "
    topsearches+=i
  strkeys=strkeys[:-3]
  strvalues=strvalues[:-3]

  keys=keys[::-1]
  values=values[::-1]

  sentPer = "Top 10 Search Queries make up " + str(topsearches) + " of " + str(totalsearches) + " total searches, which is " + str(round(topsearches/totalsearches*100)) + "% of total searches"

  averagesearchlength=round(totalsearchlength/totalsearches, 2)

  return render_template("data.html", results=keys, fvalue=values, keys=strkeys, values=strvalues, total=totalsearches, sentPer=sentPer, averageST=averagesearchlength)

@app.route("/bbml")
def bbmlRed():
  return redirect("/random")

@app.route("/random")
def bbml():

  tz_NY = pytz.timezone('America/New_York')
  now=datetime.now(tz_NY)
  OTime= now.strftime("%d/%m/%y")

  db = SQL("sqlite:///bb.db")
  result=db.execute("SELECT * FROM bb")
  
  test = open("bb.db", "a")
  test.write("")
  test.close()

  file = open("question.txt", "r")
  lines=[]

  for line in file:
    lines.append(line)

  question = lines[0]
  minmaxStr = lines[1]
  min = minmaxStr.split()[0]
  max = minmaxStr.split()[1]

  return render_template("bbml.html", results=result, question=question, min=min, max=max)

@app.route("/", methods=["GET","POST"])
def main():
  
  if request.method == "GET":
    return render_template("home.html")
  elif request.method == "POST":
    query = request.form.get("query")
    db = SQL("sqlite:///links.db")
    result=db.execute("SELECT * FROM links WHERE description LIKE :query OR name LIKE :query OR link LIKE :query", query=query)
    file_object = open('queries.txt', 'a')
    file_object.write(query+"\n")
    file_object.close()
    results2=db.execute("SELECT * FROM links")
    test = open("links.db", "a")
    test.write("")
    test.close()
    for i in results2:
      if query.lower() in i["name"].lower():
        result.append(i)
      elif query.lower() in i["description"].lower():
        result.append(i)
    return render_template("index2.html", results=result)

@app.route("/assigndj")
def assigndj():
  if not session.get("name"):
    return redirect("/")
  else:
    db = SQL("sqlite:///dj.db")
    result=db.execute("SELECT * FROM dj")
    leng=len(result)
    randNum = random.randint(2,leng)
    db = SQL("sqlite:///dj.db")
    result2=db.execute("SELECT * FROM dj WHERE id = :id", id=randNum)
    db = SQL("sqlite:///dj.db")
    db.execute("UPDATE dj SET name = :name WHERE id = :id", name=result2[0]["name"], id=1)
    
    os.remove("dj.db")
    connection = sqlite3.connect("dj.db")
    crsr = connection.cursor()
    crsr.execute("CREATE TABLE dj (id INTEGER, name TEXT NOT NULL, time, PRIMARY KEY(id))")
    connection.close()

    tz_NY = pytz.timezone('America/New_York')
    now=datetime.now(tz_NY)
    OTime= now.strftime("%d/%m/%y %H:%M:%S")

    file_object = open('djs.txt', 'a')
    file_object.write(result2[0]["name"] + " was chosen as DJ at " + OTime+"\n")
    file_object.close()

    db = SQL("sqlite:///dj.db")
    db.execute("INSERT INTO dj (name, time) VALUES(?,?)", result2[0]["name"], OTime)

    test = open("dj.db", "a")
    test.write("")
    test.close()
    
    return redirect("/dj")


@app.route("/restartbbdb")
def bbdb():
  if not session.get("name"):
    return redirect("/")
  else:   
    os.remove("bb.db")
    connection = sqlite3.connect("bb.db")
    crsr = connection.cursor()
    crsr.execute("CREATE TABLE bb (id INTEGER, name TEXT NOT NULL, guess, time, PRIMARY KEY(id))")
    connection.commit()
    crsr.close()
    connection.close()

    test = open("bb.db", "a")
    test.write("")
    test.close()
    
    return redirect("/bbml")

@app.route("/dj", methods=["GET","POST"])
def dj():
  db = SQL("sqlite:///dj.db")
  result=db.execute("SELECT * FROM dj WHERE id = :id", id=1)

  if request.method == "GET":
    return render_template("dj.html", dj=result[0]["name"], time=result[0]["time"])
  elif request.method == "POST":
    name=request.form.get("name")

    db = SQL("sqlite:///dj.db")
    db.execute("INSERT INTO dj (name) VALUES(?)", name)

    test = open("dj.db", "a")
    test.write("")
    test.close()

    return redirect("/")

@app.route("/bbentry", methods=["GET","POST"])
def bbenter():
  db = SQL("sqlite:///bb.db")
  result=db.execute("SELECT * FROM bb")

  if request.method == "GET":
    return render_template("bbml.html", results=result)
  elif request.method == "POST":
    name=request.form.get("name")
    data=request.form.get("data")
    name=name.strip()
    data=data.strip()

    tz_NY = pytz.timezone('America/New_York')
    now=datetime.now(tz_NY)
    OTime = now.strftime("%d/%m/%y")

    file = open("question.txt", "r")
    lines=[]

    for line in file:
      lines.append(line)

    minmaxStr = lines[1]
    min = int(minmaxStr.split()[0])
    max = int(minmaxStr.split()[1])

    if name!="" and data!="":
      if "," not in data:
        if int(data) >= min and int(data) <= max:
          db = SQL("sqlite:///bb.db")
          db.execute("INSERT INTO bb (name, guess, time) VALUES(?,?,?)", name, data, OTime)

          test = open("bb.db", "a")
          test.write("")
          test.close()

    return redirect("/bbml")  

@app.route("/logout")
def logout():
  session["name"] = None
  session["rank"] = None

  return redirect("/t")

@app.route("/newacc", methods=["GET","POST"])
def newaccount():
  if not session.get("name"):
    return redirect("/t")
  else:
    username = request.form.get("username")
    password = request.form.get("password")
    rank = request.form.get("rank")

    db = SQL("sqlite:///users.db")
    db.execute("INSERT INTO users (username, password, rank) VALUES(?,?,?)", username, password, rank)

    test = open("users.db", "a")
    test.write("")
    test.close()

    return redirect("/t")

@app.route("/newlink", methods=["GET","POST"])
def newact():
  if not session.get("name"):
    return redirect("/t")
  else:
    description  = request.form.get("description")
    name = request.form.get("name")
    link = request.form.get("link")

    db = SQL("sqlite:///links.db")
    db.execute("INSERT INTO links (description, name, link) VALUES(?,?,?)", description, name, link)

    test = open("links.db", "a")
    test.write("")
    test.close()

    return redirect("/t")

@app.route("/t", methods=["GET", "POST"])
def teacher():
  if not session.get("name"):
    if request.method == "GET":
      return render_template("login.html")
    elif request.method == "POST":
      username = request.form.get("username")
      password = request.form.get("password")
      db = SQL("sqlite:///users.db")
      results=db.execute("SELECT * FROM users WHERE username = :username", username=username)
      if username == os.getenv("USER") and password == os.getenv("PASS"):
        if session.get("tries") != None:
          if session.get("tries") == "0":
            tz_NY = pytz.timezone('America/New_York')
            now=datetime.now(tz_NY)
            OTime= now.strftime("%d/%m/%y %H:%M:%S")
            relTime = session.get("releaseTime")
            if relTime < OTime:
              session["tries"] = None
              session["relTime"] = None
              
            else:
              return render_template("danger.html")
          else:
            session["tries"] = None 
        session["name"] = "teacher"
        session["rank"] = "1"
        return render_template("index.html")
      elif len(results) > 0:
        if username == results[0]["username"] and password == results[0]["password"]:
         
          if session.get("tries") != None:
            if session.get("tries") == "0":
              tz_NY = pytz.timezone('America/New_York')
              now=datetime.now(tz_NY)
              OTime= now.strftime("%d/%m/%y %H:%M:%S")
              relTime = session.get("releaseTime")
              if relTime < OTime:
                session["tries"] = None
                session["relTime"] = None
               
              else:
                return render_template("danger.html")
            else:
              session["tries"] = None 

          session["name"] = "teacher/manager"
          session["rank"] = results[0]["rank"]

          return render_template("index.html")
      else:
        if session.get("tries") == None:
          session["tries"] = "1"

        elif session.get("tries") == "3":
          session["tries"] = "0"
          tz_NY = pytz.timezone('America/New_York')
          now=datetime.now(tz_NY)
          relTime = now + timedelta(minutes=5)
          OTime= relTime.strftime("%d/%m/%y %H:%M:%S")
          
          session["releaseTime"] = OTime
          return render_template("danger.html")
        
        elif session.get("tries") == "0":
          tz_NY = pytz.timezone('America/New_York')
          now=datetime.now(tz_NY)
          OTime= now.strftime("%d/%m/%y %H:%M:%S")
          relTime = session.get("releaseTime")
          if relTime < OTime:
            session["tries"] = None
            session["relTime"] = None
            return redirect("/t")
          else:
            return render_template("danger.html")

        else:
          
          tries=int(session.get("tries"))
          session["tries"] = str(tries+1)
          
        return redirect("/t")
  else:
    if session.get("tries") != None:
          if session.get("tries") == "0":
            tz_NY = pytz.timezone('America/New_York')
            now=datetime.now(tz_NY)
            OTime= now.strftime("%d/%m/%y %H:%M:%S")
            relTime = session.get("releaseTime")
            if relTime < OTime:
              session["tries"] = None
              session["relTime"] = None
           
            else:
              return render_template("danger.html")
          else:
            session["tries"] = None 
    return render_template("index.html")
 

app.run(host='0.0.0.0', port=8000)