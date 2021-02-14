import psycopg2
import werkzeug     
from werkzeug import security  

import click
from flask import current_app, g
from flask.cli import with_appcontext

def get_db():
    if 'db' not in g:
        g.db = psycopg2.connect("dbname=test user=postgres")
    return g.db

def new_user(username,password):
    conn = get_db()
    cur = conn.cursor()
    #error = None
    cur.execute(
            'INSERT INTO users (username, password) VALUES (%s, %s)',
            (username, security.generate_password_hash(password))
        )
    conn.commit()

def user_exists(username):
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
            'SELECT * FROM users WHERE username = %s', (username,)
        )
    user = cur.fetchone()
    print(user)
    if user is not None:
        return True
    else:
        return False

def get_password(username):
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
            'SELECT password FROM users WHERE username = %s', (username,)
        )
    password = cur.fetchone()
    print(password)
    return password

def get_id(username):
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        'SELECT id FROM users WHERE username = %s', (username,)
    )
    id = cur.fetchone()[0]
    print(id)
    return id

def add_post(post,username):
    conn = get_db()
    cur = conn.cursor()
    author_id = get_id(username)
    cur.execute(
        'INSERT INTO posts (post, author_id)'
        ' VALUES (%s, %s)',
        (post,author_id)
        )
    conn.commit()

def retrieve_post(username):
    conn = get_db()
    cur = conn.cursor()
    author_id = get_id(username)
    cur.execute(
    'SELECT post FROM posts WHERE author_id = %s', (author_id,)
    )
    post = cur.fetchmany()
    return post

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    db = get_db()
    cur = db.cursor()

    with current_app.open_resource('schema.sql') as f:
        cur.executemany(f.read().decode('utf8'),[])
    db.commit()

@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)