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
    cur.commit()

def user_exists(username):
    conn = get_db()
    cur = conn.cursor()
    user = cur.execute(
            'SELECT * FROM users WHERE username = %s', (username,)
        )
    print(user)
    if user is not None:
        return True
    else:
        return False

def get_password(username):
    datab = get_db()
    password = datab.execute(
            'SELECT password FROM users WHERE username = %s', (username,)
        ).fetchone()
    return password

def add_post(post):
    conn = get_db()
    print(conn)
    with conn.cursor() as cur:
        cur.execute(
            'INSERT INTO posts (post, author_id)'
            ' VALUES (?, ?)',
            (post, g.user['id'])
        )
    conn.commit()

def retrieve_post():
    conn = get_db()
    with conn.cursor() as cur:
        cur.execute(
        'SELECT post FROM posts WHERE author_id = ?', (g.users['id'],)
        ).fetchone()

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