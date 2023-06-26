from flask import Flask, render_template, request, redirect, g
import sqlite3
import os

app = Flask(__name__)
db_file = 'database.db'

# Check if the database file exists
if not os.path.exists(db_file):
    # Create the database, users table, and salads table
    db = sqlite3.connect(db_file)
    db.execute('CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT)')
    db.execute('CREATE TABLE salads (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, price REAL, description TEXT)')

    # Add some example salads
    db.execute("INSERT INTO salads (name, price, description) VALUES (?, ?, ?)", ('Caesar', 9.99, 'Classic Caesar salad with romaine lettuce, croutons, and Caesar dressing'))
    db.execute("INSERT INTO salads (name, price, description) VALUES (?, ?, ?)", ('Greek', 8.99, 'Traditional Greek salad with tomatoes, cucumbers, onions, olives, and feta cheese'))
    db.execute("INSERT INTO salads (name, price, description) VALUES (?, ?, ?)", ('Caprese', 10.99, 'Fresh Caprese salad with tomatoes, mozzarella cheese, and basil'))
    db.execute("INSERT INTO users (username, password) VALUES (?, ?)", ('root', 'root'))
    db.commit()

@app.before_request
def before_request():
    g.db = sqlite3.connect(db_file)

@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()

@app.route('/')
def home():
    # Retrieve all salads from the database
    cursor = g.db.execute("SELECT * FROM salads")
    salads = cursor.fetchall()
    return render_template('home.html', salads=salads)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cursor = g.db.execute(f"SELECT * FROM users WHERE username='{username}' AND password='{password}'")
        user = cursor.fetchone()

        if user is not None:
            return redirect('/profile')
        else:
            return render_template('login.html', error=True)
    else:
        return render_template('login.html', error=False)

@app.route('/profile')
def profile():
    return render_template('profile.html')

if __name__ == '__main__':
    app.run()
