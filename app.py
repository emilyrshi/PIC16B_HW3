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
           message text
       )''')
      g.message_db.commit()
      g.message_db.close()
      return g.message_db 


def insert_message(request):
  handle_input = request.form["handle"]
  message_input = request.form["message"]
  cursor.execute("INSERT INTO messages (handle, message) VALUES (%(handle_input)s, %(message_input)s)")
  g.message_db.commit()
  g.message_db.close()


@app.route("/ask/", methods=['POST', 'GET'])
def renders():
    if request.method == 'GET':
        # if the user just visits the url
        return render_template('submit.html')
    else:
        insert_message()
        return render_template('submit.html')


def random_messages(n):
  """
  Returns a collection of n random messages from the message_db (or fewer if necessary)
  """
  SELECT message FROM messages ORDER BY RANDOM() LIMIT n;

  f = open('view.html','w')
  
  random_messages = message
  
  f.write(random_messages)
  f.close()

  g.message_db.commit()
  g.message_db.close()

