import sqlite3
from flask import Flask, render_template, request
from flask import redirect, url_for, abort

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
           message text, 
       )''')
      return g.message_db 
     
g.message_db.commit()
g.message_db.close()


def insert_message(request):
  
  return

@app.route("/ask/", methods=['POST', 'GET'])
def ask():
    if request.method == 'GET':
        # if the user just visits the url
        return render_template('ask.html')
    else:
        # if the user submits the form
        name = request.form['name']
        student = request.form['student']
        return render_template('ask.html', name=name, student=student)
