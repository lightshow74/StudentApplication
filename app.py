# https://www.tutorialspoint.com/flask/flask_sqlite.htm
# http://flask.pocoo.org/docs/0.12/patterns/sqlite3/
# https://github.com/stevedunford/NZVintageRadios

import sqlite3
from flask import Flask, Response, render_template, abort, url_for
from flask_admin import Admin
from wtforms import Form, RadioField, BooleanField, StringField, PasswordField, validators
from flask_sqlalchemy import SQLAlchemy

# Creates a Flask object called 'app' that we can use throughout the programme
app = Flask(__name__)

# DB Connection
def query_db(query, single=False):
    db = sqlite3.connect('db/report.db')
    cursor = db.cursor()
    cursor.execute(query)
    result = cursor.fetchone() if single else cursor.fetchall()
    return result

# This is the function that controls the main page of the web site
@app.route("/")
def index():
  query = query_db("SELECT Students.StudentID, Students.StudentName, StandardID, AssessedLevel from Assessment join Students using (StudentID)")
  students = [dict(studentID=row[0], studentName=row[1], standardID=row[2], assessedLevel=row[3]) for row in query]

  return render_template('students.html',
                          title="Progress Report",
                          students=students)

'''
# This is the function shows the Student page
@app.route("/students")
def students():
  query = query_db("SELECT StudentID, StudentName from Students")
  students = [dict(studentID=row[0], studentName=row[1]) for row in query]

  return render_template('students.html',
                          title="Students",
													students=students)
'''

# Function that displays the individual report for a student
@app.route("/students/<int:id>")
def student_edit(id): # Function definition contains a parameter for ID
  single="TRUE"
## Database Query where ID is selected from a link in the GUI
  query = query_db("SELECT Students.StudentID, Students.StudentName, StandardID, Standards.StandardTitle, AssessedLevel from Assessment join Students using (StudentID) join Standards using (StandardID) WHERE Students.StudentID={0} ".format(id), single)

  standards_query = query_db("SELECT StandardID, Standards.StandardTitle, AssessedLevel from Assessment join Students using (StudentID) join Standards using (StandardID) WHERE Students.StudentID={0} ".format(id))
  standards= [dict(StandardID=row[0], StandardTitle=row[1], AssessedLevel=row[2]) for row in standards_query]


  skills_query = query_db("SELECT SkillSetID, Skills.SkillTitle, SkillWorkshop from SkillSet join Skills using (SkillID) join Students using (StudentID) WHERE Students.StudentID={0} ".format(id))

  skills= [dict(SkillSetID=row[0], SkillTitle=row[1], SkillWorkshop=row[2]) for row in skills_query]

  projects_query = query_db("SELECT ProjectTitle from Project join Students using (StudentID) WHERE Students.StudentID={0} ".format(id))

  projects= [dict(ProjectTitle=row[0]) for row in projects_query]

## Page Not Found 
  if not query:
    abort(404)

  return render_template('report.html',
                          title="Student Report",
                          student=query,
                          standards=standards,
                          skills=skills,
                          projects=projects,
                          id=id)



# This function deals with any missing pages and shows the Error page
@app.errorhandler(404)
def page_not_found(e):
  return render_template('404.html', title="404"), 404

if __name__ == "__main__":
    app.run(debug=True)



