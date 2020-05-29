import os
import subprocess
import random
import json
import shlex
import sqlite3
import secrets
from flask import render_template, flash
from werkzeug.security import generate_password_hash, check_password_hash
from SensitiveData import PROJECT_EMAIL, PROJECT_PASSWORD
from simple_mail import send_email

# If on windows, don't try to run the shell scripts.
if os.name == 'nt':
    class subprocess():
        def call(self, *args, **kwargs):
            return True


def set_account_validity(username, validity):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    with conn:
        cur.execute("""UPDATE accounts SET pending_verification=0 WHERE username=:username""",  {
                    'username': username})


def generate_token(username, tokentype):
    token = secrets.token_urlsafe(64)
    with open('text/active_reset_tokens.json') as file:
        reset_dictionary = file.read()
    reset_dictionary = json.loads(reset_dictionary)
    reset_dictionary[tokentype][token] = username
    reset_dictionary = json.dumps(
        reset_dictionary, sort_keys=True, indent=4, separators=(',', ': '))
    with open('text/active_reset_tokens.json', 'w') as file:
        file.write(reset_dictionary)
    return token


def check_token(token, tokentype):
    with open('text/active_reset_tokens.json') as file:
        valid_token_dictionary = file.read()
    valid_token_dictionary = json.loads(valid_token_dictionary)
    return token in valid_token_dictionary[tokentype]


def remove_token(token, tokentype):
    with open('text/active_reset_tokens.json') as file:
        valid_token_dictionary = file.read()
    valid_token_dictionary = json.loads(valid_token_dictionary)
    valid_token_dictionary[tokentype].pop(token)
    valid_token_dictionary = json.dumps(
        valid_token_dictionary, sort_keys=True, indent=4, separators=(',', ': '))
    print(valid_token_dictionary)
    with open('text/active_reset_tokens.json', 'w') as file:
        file.write(valid_token_dictionary)


def get_user_from_token(token, tokentype):
    with open('text/active_reset_tokens.json') as file:
        valid_token_dictionary = file.read()
    valid_token_dictionary = json.loads(valid_token_dictionary)
    return valid_token_dictionary.get(tokentype).get(token, "")


def generate_valid_code():
    with open('text/validcodes.txt', 'r') as file:
        VALID_CODES = file.readline()
    random_number = random.randint(0, len(VALID_CODES)-5)
    code = VALID_CODES[random_number:random_number+5]
    return code


def create_account(username, password, recovery_email, prayer_groups, bad_password):
    # Create user files and folders
    os.makedirs("userdata/{}/writer/documents/".format(username))
    os.makedirs("userdata/{}/writer/thumbnails/".format(username))
    os.makedirs('userdata/{}/todo/'.format(username))
    open("userdata/{}/todo/list.csv".format(username), 'a').close()
    # Add database entry
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    with conn:
        cur.execute("""
            INSERT INTO accounts
            (username, hashed_password, have_access_to, recovery_email, prayer_groups, prayer_email, pending_verification) 
            VALUES (:username, :hashed_password, :have_access_to, :recovery_email, :prayer_groups, :prayer_email, :pending_verification)""",

                    {
                        'username': username,
                        'hashed_password': generate_password_hash(password),
                        'have_access_to': '',
                        'recovery_email': recovery_email,
                        'prayer_groups': prayer_groups,
                        'prayer_email': recovery_email,
                        'pending_verification': 1

                    })
    # Create a new linux user.
    subprocess.call(shlex.split(
        "sudo sh ./new_linux_user.sh {} {}".format(username, password)))
    # Generate a verification code.
    token = generate_token(username, "new_account")
    with open('text/account_verification_email_template.html') as file:
        VERIFICATION_EMAIL_TEMPLATE = file.read()
    if bad_password:
        BAD_PW_MESSAGE = "By the way, we noticed you're using a pretty short password. Consider changing it to a longer one later!"
    else:
        BAD_PW_MESSAGe = ""
    message = VERIFICATION_EMAIL_TEMPLATE.format(
        token=token, username=username, additional_messages=BAD_PW_MESSAGE)
    send_email(recovery_email, "Thanks for signing up for jforseth.tech!",
               message, PROJECT_EMAIL, PROJECT_PASSWORD)


def delete_account(username):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    with conn:
        cur.execute("""
            DELETE FROM accounts WHERE username=:username""",
                    {'username': username, })
    subprocess.call(shlex.split(
        "sudo sh ./delete_user.sh {}".format(username)))
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
    elif user_data.get('pending_verification') == 1:
        flash("This account hasn't been verified. Check your email.")
        return False
    elif check_password_hash(user_data.get('hashed_password'), user['password']):
        return True  # <--- user is logged in!

    else:
        flash("Incorrect password.")
        return False  # <--- invalid credentials
# TODO: Find a way to encrypt user data.
# TODO: Mail account frontend.
# TODO: Merge mail, PR, and general accounts.

# Get the areas of the site the user currently has access to.


def get_current_access(username):
    user_data = get_account(username)
    return user_data["have_access_to"].split(',')


def check_code(code):
    with open('text/validcodes.txt', 'r') as file:
        valid_codes = file.readline()

    if code in valid_codes:
        code_validity = True
    else:
        code_validity = False
    new_code = str(random.randint(10000, 99999))
    valid_codes = valid_codes.replace(code, new_code)
    with open('text/validcodes.txt', 'w') as file:
        file.write(valid_codes)
    return code_validity


def update_pw(current_username, new_plain_password):
    new_hashed_password = generate_password_hash(new_plain_password)
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    with conn:
        cur.execute("""
            UPDATE accounts
            SET hashed_password=:new_hashed_password
            WHERE username=:current_username""",

                    {'new_hashed_password': new_hashed_password,
                     'current_username': current_username})
    subprocess.call(shlex.split(
        "sudo sh ./change_pw.sh {} {}".format(current_username, new_plain_password)))
# Checks if user has to a specific area.
# Used by @login_required decorator.
# def have_access_to_writer(username):
#    user_data = get_account(username)
#    if 'writer' not in user_data.get('have_access_to'):
#        return render_template("errors/403.html")

def change_email(username, email, email_type):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    with conn:
        cur.execute("""UPDATE accounts SET {email_type}='{email}' WHERE username='{username}'""".format(email_type=email_type,email=email, username=username))
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
