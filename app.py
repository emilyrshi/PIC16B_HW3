from flask import Flask, render_template, request, g
from flask import redirect, url_for, abort
import sqlite3

app = Flask(__name__)

def get_message_db():
    try:
        return g.message_db
    except AttributeError:
        g.message_db = sqlite3.connect("message_db.sqlite")
        cursor = g.message_db.cursor()
        # creates a table with columns for "handle" and "message"
        cursor.execute('''CREATE TABLE IF NOT EXISTS messages (
                              id INTEGER PRIMARY KEY,
                              handle TEXT,
                              message TEXT)''')
        g.message_db.commit()
        return g.message_db
    
def insert_message(request):
    message = request.form['message']
    handle = request.form['handle']
    
    # Get the database connection
    db = get_message_db()
    
    cursor = db.cursor()
    
    # SQL query to insert the message into the 'messages' table
    insert_query = "INSERT INTO messages (handle, message) VALUES (?, ?)"
        
    # Execute the SQL query with the handle and message as parameters
    cursor.execute(insert_query, (handle, message))
    
    # Commit the changes to the database
    db.commit()
    db.close()
    
def random_messages(n):
    
    # Get the database connection
    db = get_message_db()
    
    # Create a cursor object to execute SQL commands
    cursor = db.cursor()    
    
    # SQL query to insert the message into the 'messages' table
    cursor.execute('''SELECT handle, message FROM messages ORDER BY RANDOM() LIMIT ?''', (n,))
    messages = cursor.fetchall()
   
    # Commit the changes to the database
    db.close()
    
    return messages

@app.route('/')
def main():
    return render_template('base.html')
    
@app.route('/submit', methods=['GET', 'POST'])
def submit():
    # POST used to send data to a server to create/update
    if request.method == 'POST':
        # this function handles inserting a user message into the db
        insert_message(request)
        # render submit.html 
        return render_template('submit.html')
    else:
        # if nothing is posted, just render the same page again
        return render_template('submit.html')
    
@app.route('/view')
def view():
    # grabs 5 (or less) random messages 
    rand_mess = random_messages(5)
    # passes the messages as an argument to render_template()
    return render_template('view.html', rand_mess = rand_mess)

if __name__ == '__main__':
    app.run(debug=True)
