import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from flask import render_template, flash
import os
import subprocess
#import crypt
import shlex
if os.name=='nt':
    class subprocess():
        def call(*args, **kwargs):
            return True
def verify_email():
    
def create_account(username, password):
    os.makedirs("userdata/{}/writer/documents/".format(username))
    os.makedirs("userdata/{}/writer/thumbnails/".format(username))
    os.makedirs('userdata/{}/todo/'.format(username))
    open("userdata/{}/todo/list.csv".format(username),'a').close()
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    with conn:
        cur.execute("""
            INSERT INTO accounts
            (username, hashed_password, have_access_to) VALUES (:username, :hashed_password, :have_access_to)""",
        
            {
                'username':username,
                'hashed_password':generate_password_hash(password),
                'have_access_to':''
            })
    #Create a new linux user.
    subprocess.call(shlex.split("sudo sh ./new_linux_user.sh {} {}".format(username,password)))

def delete_account(username):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    with conn:
        cur.execute("""
            DELETE FROM accounts WHERE username=:username""",
            {'username':username,})
    subprocess.call(shlex.split("sudo sh ./delete_user.sh {}".format(username)))

# Retrieve all date on a given user. Returns a dict with columns as keys.
def get_account(username):
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    
    cur.execute("""SELECT * FROM accounts WHERE username=:username""",
                {'username': username})
    
    account_data = cur.fetchone()
    
    if account_data == None:
        return {}
    
    return dict(zip(account_data.keys(), account_data))


# Check if a given username and password is valid.
def check_login(user):
    user_data = get_account(user['username'])

    if not user_data:
        flash("Account not found", category="warning")
        return False  # <--- invalid credentials, no data

    elif check_password_hash(user_data.get('hashed_password'), user['password']):
        return True  # <--- user is logged in!

    else:
        return False  # <--- invalid credentials
#TODO: Find a way to encrypt user data.
#TODO: Mail account frontend.
#TODO: Merge mail, PR, and general accounts.

# Get the areas of the site the user currently has access to.
def get_current_access(username):
    user_data = get_account(username)
    return user_data["have_access_to"].split(',')

def update_pw(current_username, new_plain_password):
    new_hashed_password=generate_password_hash(new_plain_password)
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    with conn:
        cur.execute("""
            UPDATE accounts
            SET hashed_password=:new_hashed_password
            WHERE username=:current_username""",
        
            {'new_hashed_password':new_hashed_password,
            'current_username':current_username})
    subprocess.call(shlex.split("sudo sh ./change_pw.sh {} {}".format(current_username,new_plain_password)))
# Checks if user has to a specific area.
# Used by @login_required decorator.
#def have_access_to_writer(username):
#    user_data = get_account(username)
#    if 'writer' not in user_data.get('have_access_to'):
#        return render_template("errors/403.html")
def have_access_to_todo(username):
    user_data = get_account(username)
    if 'todo' not in user_data.get('have_access_to'):
        return render_template("errors/403.html")

def have_access_to_admin(username):
    user_data = get_account(username)
    if 'admin' not in user_data.get('have_access_to'):
        return render_template("errors/403.html")

def have_access_to_lqa(username):
    user_data = get_account(username)
    if 'lqa' not in user_data.get('have_access_to'):
        return render_template("errors/403.html")

if __name__ == "__main__":
    print("The function to check user authentication using flask_simplelogin")
