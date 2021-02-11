import werkzeug     
from werkzeug import security  

def get_username(user):
  return None
def new_user(username, password):
  return 0
def get_password(username):
  pw =  '1234'
  hash = security.generate_password_hash(pw)
  return hash
def save_post(user,body):
  return None