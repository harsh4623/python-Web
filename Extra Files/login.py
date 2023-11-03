from flask import Flask, render_template, request, redirect, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import subprocess

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

import sys

# Define a function to run app_new.py
def run_app_new():
    try:
        # Get the full path to the Python executable
        python_executable = sys.executable

        # Run the app_new.py script using subprocess
        subprocess.run([python_executable, "/Users/harshpatel/Desktop/Final_Project/website/app_new.py"], check=True, text=True)
    except subprocess.CalledProcessError as e:
        print("Error running app_new.py:", e)

# def run_app_new():
#     try:
#         # Run the app_new.py script using subprocess
#         subprocess.run(["python", "app_new.py"], check=True, text=True)
#     except subprocess.CalledProcessError as e:
#         print("Error running app_new.py:", e)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the username is already taken
        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username is already taken. Please choose another.')
        else:
            # Hash the password before storing it in the database
            hashed_password = generate_password_hash(password)
            new_user = User(username=username, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful. You can now log in.')
            return redirect('/login')
    
    return render_template('register.html')

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session["user_id"] = user.id
            flash("Login successful.")
            
            # Run app_new.py here
            return render_template('layout.html')
            # run_app_new()
            
            # return redirect("/profile")
        else:
            flash("Login failed. Please check your username and password.")

    return render_template("login.html")

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']

#         user = User.query.filter_by(username=username).first()
#         if user and check_password_hash(user.password, password):
#             session['user_id'] = user.id
#             flash('Login successful.')
#             return redirect('/profile')
#         else:
#             flash('Login failed. Please check your username and password.')

#     return render_template('login.html')

@app.route('/profile')
def profile():
    if 'user_id' in session:
        user = User.query.filter_by(id=session['user_id']).first()
        return f'Logged in as {user.username}'
    else:
        return 'You are not logged in.'

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect('/')

if __name__ == '__main__':
    # db.create_all()
    with app.app_context():
        # Create the database tables
        db.create_all()
    app.run(debug=True)
