from flask import Flask, render_template, request
import sqlite3 as sql
app = Flask(__name__)

from flask import Flask, g, render_template, request

import sklearn as sk
import matplotlib.pyplot as plt
import numpy as np
import pickle
import os
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

import io
import base64

app = Flask(__name__)

@app.route("/create_db/") # decorators
def get_message_db():
  # write some helpful comments here
  try:
      # check whether a table called messages exists in message_db
      cursor.execute("SELECT * FROM messages")
      return g.message_db
  except:
      g.message_db = sqlite3.connect("messages_db.sqlite")      
      cursor = g.message_db.cursor()
      cursor.execute('''
       CREATE TABLE messages(
           handle text,
           message text
       )''')
      return g.message_db 

@app.route("/insert/") # decorators
def insert_message(request):
  handle_input = request.form["handle"]
  message_input = request.form["message"]
  cursor.execute("INSERT INTO messages (handle, message) VALUES (%(handle_input)s, %(message_input)s)")
  g.message_db.commit()
  g.message_db.close()
  

@app.route("/submit/", methods=['POST', 'GET'])
def submit():
    if request.method == 'GET':
        # if the user just visits the url
        return render_template('submit.html')
    else:
        # if the user submits the form
        insert_message()
        return render_template('submit.html')
      #   try:
      #     insert_message()
      #    with sql.connect("messages_db.sqlite") as con:
      #       cur = con.cursor()
            
      #       # ADD CODE HERE
      #       cur.execute("CODE HERE")
            
      #       con.commit()
      #       msg = "Record successfully added"
      # except:
      #    con.rollback()
      #    msg = "error in insert operation"
      
      # finally:
      #    return render_template("result.html",msg = msg)
      #    con.close()

@app.route("/rand_mes/") # decorators
def random_messages(n):
  """
  Returns a collection of n random messages from the message_db (or fewer if necessary)
  """
  g.message_db = sqlite3.connect("messages_db.sqlite")      
  cursor = g.message_db.cursor()
  # cursor.execute("SELECT handle, messages FROM messages ORDER BY RANDOM() LIMIT n")
  cursor.execute("SELECT handle, messages FROM messages")
  random_messages = cursor.fetchall()

  g.message_db.commit()
  g.message_db.close()

  return random_messages


@app.route("/ask/", methods=['POST', 'GET'])
def renders():
    if request.method == 'GET':
        # if the user just visits the url
        randMess = random_messages(5)
        return render_template('view.html', random_messages = randMess)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
