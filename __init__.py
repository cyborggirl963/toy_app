from toy_app.db import get_password
from flask import Flask, request, url_for, session, g, redirect, flash
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)

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
        elif get_username() is not None:
            error = 'User {} is already registered.'.format(username)
        flash(error)
    return """
    <!doctype html>
    <form method="POST">
        <label>User: <input name="username" /></label>
        <label>User: <input name="password" type="password" /></label>
        <input type="submit" />
    </form> """

@app.route('/login', methods=['POST', 'GET'])
def login():
    #needs finishing
    #not sure what to do about error message
    error = None
    if request.method == 'POST':
        request.form['username']
        request.form['password']
        error = None
        password = get_password() 
        
        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('my_pantry.upload'))

        flash(error)
            #error = 'Invalid username/password'
    # the code below is executed if the request method
    # was GET or the credentials were invalid
    return """
    <!doctype html>
    <form method="POST">
        <label>User: <input name="username" /></label>
        <label>User: <input name="password" type="password" /></label>
        <input type="submit" />
    </form> """




    