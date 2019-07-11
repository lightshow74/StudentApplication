# https://www.tutorialspoint.com/flask/flask_sqlite.htm
# http://flask.pocoo.org/docs/0.12/patterns/sqlite3/
# https://github.com/stevedunford/NZVintageRadios

import sqlite3
from flask import Flask, Response, render_template, abort

# Creates a Flask object called 'app' that we can use throughout the programme
app = Flask(__name__)

# This is the function that controls the main page of the web site
@app.route("/")
def index():
  return render_template('main.html',
                          title="Progress Report")

'''
# This is the function shows the Athletes page
@app.route("/athletes")
def athletes():

  conn = sqlite3.connect('db/medals.db')
  cursor = conn.cursor()
  results = cursor.execute("SELECT * from Medalists")
  medalists = [dict(id=row[0], medal=row[1], firstname=row[2], lastname=row[3], event=row[4]) for row in results]

  return render_template('athletes.html',
                          title="Athletes",
													medalists=medalists)

'''

# This function deals with any missing pages and shows the Error page
@app.errorhandler(404)
def page_not_found(e):
  return render_template('404.html', title="404"), 404

if __name__ == "__main__":
    app.run(debug=True)



