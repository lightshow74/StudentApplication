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
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/josh/Projects/StudentApplication/db/report.db'
db = SQLAlchemy(app)

# DB Connection
def query_db(query, single=False):
    
    cursor = db.cursor()
    cursor.execute(query)
    result = cursor.fetchone() if single else cursor.fetchall()
    return result

# This is the function that controls the main page of the web site
@app.route("/")
def index():
  query = query_db("SELECT Students.StudentName, StandardID, AssessedLevel from Assessment join Students using (StudentID)")
  assessment = [dict(student=row[0], standard=row[1], assessed=row[2]) for row in query]

  return render_template('assessment.html',
                          title="Progress Report",
                          assessment=assessment)

# This is the function shows the Student page
@app.route("/students")
def students():
  query = query_db("SELECT StudentID, StudentName from Students")
  students = [dict(studentID=row[0], studentName=row[1]) for row in query]

  return render_template('students.html',
                          title="Students",
													students=students)


# This function deals with any missing pages and shows the Error page
@app.errorhandler(404)
def page_not_found(e):
  return render_template('404.html', title="404"), 404

if __name__ == "__main__":
    app.run(debug=True)



