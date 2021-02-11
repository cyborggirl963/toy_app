#from .db import get_password
from . import db_mock
from flask import Flask, request, url_for, session, g, redirect, flash
import werkzeug     
from werkzeug import security  

app = Flask(__name__)
app.config.update(
    TESTING=True,
    SECRET_KEY='987654321'
)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/register',methods=['GET','POST'])
def register():
    #needs finishing
    #removed return at the end with template stuff 
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif db_mock.get_username(username) is not None:
            error = 'User {} is already registered.'.format(username)

        if error is None:
            db_mock.new_user(username,password)
            return redirect(url_for('login'))
        flash(error)
    return """
    <!doctype html>
    <h1>Registration page</h1>
    <form method="POST">
        <label>Username: <input name="username" /></label>
        <label>Password: <input name="password" type="password" /></label>
        <input type="submit" />
    </form> """

@app.route('/login', methods=['POST', 'GET'])
def login():
    #needs finishing
    #not sure what to do about error message
    error = None
    if request.method == 'POST':
        user = request.form['username']
        pw = request.form['password']
        error = None
        password = db_mock.get_password(user) 
        
        if user is None:
            error = 'Incorrect username.'
        elif not security.check_password_hash(password, pw):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['username'] = user
            return redirect(url_for('post'))

        flash(error)
            #error = 'Invalid username/password'
    # the code below is executed if the request method
    # was GET or the credentials were invalid
    return """
    <!doctype html>
    <h1>Login page</h1>
    <form method="POST">
        <label>Username: <input name="username" /></label>
        <label>Password: <input name="password" type="password" /></label>
        <input type="submit" />
    </form> """

@app.route('/post', methods=['POST', 'GET'])
def post():
    if request.method == 'POST':
        body = request.form['post']
        error = None

        if body is None:
            error = 'Post text is required'

        if error is None:
            db_mock.save_post(session['username'],body)
            return 'Success!'

    return """
    <!doctype html>
    <h1>Write post</h1>
    <form method="POST">
        <textarea rows="4" cols="50" name="post">
        </textarea>
        <input type="submit"/>
    </form> """