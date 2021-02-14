#from .db import get_password
from . import db_mock
from . import db
from flask import Flask, request, url_for, session, g, redirect, flash
import werkzeug     
from werkzeug import security

app = Flask(__name__)
app.config.update(
    TESTING=True,
    SECRET_KEY='987654321'
)

from . import db
db.init_app(app)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/register',methods=['GET','POST'])
def register():
    #needs finishing
    #removed return at the end with template stuff 
    error = ""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        #error = ""

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif db.user_exists(username):
            error = 'User {} is already registered.'.format(username)

        else:
            db.new_user(username,password)
            return redirect(url_for('login'))
        flash(error)
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
    <title>Registration Page</title>
    <style type="text/css">
     .error:empty {{
        display: none;
    }}
    </style>
    </head>
    <body>
    <h1>Registration Page</h1>
    <div class="error">{error}</div>
    <form method="POST">
        <label>Username: <input name="username" /></label>
        <label>Password: <input name="password" type="password" /></label>
        <input type="submit" />
    </form> 
    </body>
    </html>
    """

@app.route('/login', methods=['POST', 'GET'])
def login():
    #needs finishing
    #not sure what to do about error message
    error = ""
    if request.method == 'POST':
        user = request.form['username']
        pw = request.form['password']
        print(security.generate_password_hash(pw))
        print(pw)
        password = db.get_password(user)[0] 
        
        if user is None:
            error = 'Incorrect username.'
            print(error)
        elif not security.check_password_hash(password,pw):
            error = 'Incorrect password.'
            print(error)

        if error is "":
            session.clear()
            session['username'] = user
            return redirect(url_for('post'))

            #error = 'Invalid username/password'
    # the code below is executed if the request method
    # was GET or the credentials were invalid
    return """
    <!doctype html>
    <h1>Login page</h1>
    <form method="POST">
        <label>Username: <input name="username" /></label>
        <label>Password: <input name="password" type="password" /></label>
        <input type="submit"/>
    </form> """

@app.route('/post', methods=['POST', 'GET'])
def post():
    if request.method == 'POST':
        body = request.form['post']
        error = None

        if body is None:
            error = 'Post text is required'

        if error is None:
            db.add_post(body,session['username'])
            return redirect(url_for('success'))

    return """
    <!doctype html>
    <h1>Write post</h1>
    <form method="POST">
        <textarea rows="4" cols="50" name="post">
        </textarea>
        <input type="submit"/>
    </form> """

@app.route('/success', methods=['POST', 'GET'])
def success():
    post_text = db.retrieve_post(session['username'])
    if request.method == 'POST':
        return redirect(url_for('post'))

    return f"""
    <!doctype html>
    <html>
    <head
    <h1>Success! Your post:</h1>
    </head>
    <body>
        {post_text}
    <form method="POST">
        <input type="submit"/>
    </form>
    </body>
    </html>
    """