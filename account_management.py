import os
import subprocess
import random
import json
import shlex
import sqlite3
import secrets
from flask import render_template, flash, escape, Markup
from werkzeug.security import generate_password_hash, check_password_hash
from SensitiveData import PROJECT_EMAIL, PROJECT_PASSWORD
from simple_mail import send_email
from werkzeug.utils import secure_filename

# If on windows, don't try to run the shell scripts.
# HACK: When subprocess is called,
#       it goes to this class
#       not the subprocess module.
if os.name == 'nt':
    class subprocess():
        def call(self, *args, **kwargs):
            return True


def set_account_validity(username, validity):
    """Sets the validity of a newly created account.

    Arguments:
        username {str} -- The username to modify
        validity {int} -- 1 for invalid, 0 for valid.
    """
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    with conn:
        cur.execute("""UPDATE accounts SET pending_verification=0 WHERE username=:username""",  {
                    'username': username})


def generate_token(username, tokentype):
    """Create a token to verify the legitimacy of a jforseth.tech link.

    Arguments:
        username {str} -- The username to issue the token too. Email addresses also work.
        tokentype {str} -- The type of token issued. Check the active_tokens.json file for valid tokentypes.

    Returns:
        str -- A token
    """
    token = secrets.token_urlsafe(64)
    #json file:
    #{
    #   tokentype:{token:user}
    #}
    with open('text/active_tokens.json') as file:
        reset_dictionary = file.read()
    reset_dictionary = json.loads(reset_dictionary)
    reset_dictionary[tokentype][token] = username
    # Prettify the json output.
    reset_dictionary = json.dumps(
        reset_dictionary, sort_keys=True, indent=4, separators=(',', ': '))
    with open('text/active_tokens.json', 'w') as file:
        file.write(reset_dictionary)
    return token


def check_token(token, tokentype):
    """Checks that a given token and type are valid in the active_tokens.json file.

    Arguments:
        token {str} -- The token to check
        tokentype {str} -- The type of token being checked

    Returns:
        bool -- Whether or not the token is valid.
    """
    #json file:
    #{
    #   tokentype:{token:user}
    #}
    with open('text/active_tokens.json') as file:
        valid_token_dictionary = file.read()
    valid_token_dictionary = json.loads(valid_token_dictionary)
    return token in valid_token_dictionary[tokentype]


def remove_token(token, tokentype):
    """Delete a token that has be "used up"

    Arguments:
        token {str} -- The token to remove
        tokentype {str} -- The type of token being removed.
    """
    #json file:
    #{
    #   tokentype:{token:user}
    #}
    with open('text/active_tokens.json') as file:
        valid_token_dictionary = file.read()
    valid_token_dictionary = json.loads(valid_token_dictionary)
    valid_token_dictionary[tokentype].pop(token)
    #Prettify the json output.
    valid_token_dictionary = json.dumps(
        valid_token_dictionary, sort_keys=True, indent=4, separators=(',', ': '))
    print(valid_token_dictionary)
    with open('text/active_tokens.json', 'w') as file:
        file.write(valid_token_dictionary)


def get_user_from_token(token, tokentype):
    """Retrieve the username the token was issued to.

    Arguments:
        token {str} -- The token being checked.
        tokentype {str} -- The type of token.

    Returns:
        str -- The username
    """
    #json file:
    #{
    #   tokentype:{token:user}
    #}
    with open('text/active_tokens.json') as file:
        valid_token_dictionary = file.read()
    valid_token_dictionary = json.loads(valid_token_dictionary)
    return valid_token_dictionary.get(tokentype).get(token, "")

# This was used in place of tokens before
# I realized it was a joke to brute force.
#def generate_valid_code():
#    """DEPRECIATED. DO NOT USE.
#
#    Returns:
#        str -- A five-digit string of integers.
#    """
#    with open('text/validcodes.txt', 'r') as file:
#        VALID_CODES = file.readline()
#    random_number = random.randint(0, len(VALID_CODES)-5)
#    code = VALID_CODES[random_number:random_number+5]
#    return code


def create_account(username, password, recovery_email, prayer_groups, bad_password):
    """Create a new account.

    Arguments:
        username {str} -- The username of the new account
        password {str} -- The user's password in plaintext.
        recovery_email {str} -- The user's email address. (Used for recovery_email AND prayer_email on account creation.)
        prayer_groups {str} -- The prayer groups the user is a part of. Separated by a '|'.
        bad_password {bool} -- Whether or not the user is using an insecure password.
    """
    # Create user files and folders
    username=username.encode('utf-8')
    os.makedirs("userdata/{}/writer/documents/".format(username))
    os.makedirs("userdata/{}/writer/thumbnails/".format(username))
    os.makedirs('userdata/{}/todo/'.format(username))
    open("userdata/{}/todo/list.csv".format(username), 'a').close()

    # Add database entry
    username=username.decode('utf-8')
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
    password=password.encode('utf-8')
    username=username.encode('utf-8')
    subprocess.call(shlex.split(
        "sudo sh ./new_linux_user.sh {} {}".format(username, password)))

    token = generate_token(username, "new_account")
    # Create a verification email.
    with open('text/account_verification_email_template.html') as file:
        VERIFICATION_EMAIL_TEMPLATE = file.read()
    #Append this to the message if the user chooses a weak password:
    BAD_PW_MESSAGE=""
    if bad_password:
        BAD_PW_MESSAGE = "By the way, we noticed you're using a pretty short password. Consider changing it to a longer one later!"
    message = VERIFICATION_EMAIL_TEMPLATE.format(
        token=token, username=username, additional_messages=BAD_PW_MESSAGE)
    send_email(recovery_email, "Thanks for signing up for jforseth.tech!",
               message.encode('utf-8'), PROJECT_EMAIL, PROJECT_PASSWORD)


def delete_account(username):
    """Remove an account.

    Arguments:
        username {str} -- The username to remove.
    """
    # Delete database entry
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    # Delete UNIX user and user files.
    with conn:
        cur.execute("""
            DELETE FROM accounts WHERE username=:username""",
                    {'username': username, })
    subprocess.call(shlex.split(
        "sudo sh ./delete_user.sh {}".format(username)))
# Retrieve all date on a given user. Returns a dict with columns as keys.


def get_account(username):
    """Retrieve a user's account data.

    Arguments:
        username {str} -- The username to retrieve data on.

    Returns:
        dict -- A dictionary with column names as keys, and account data as values.
    """
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute("""SELECT * FROM accounts WHERE username=:username""",
                {'username': username})

    account_data = cur.fetchone()

    if account_data == None:
        return {}
    #TODO: What does this line do?
    return dict(zip(account_data.keys(), account_data))


# Check if a given username and password is valid.
def check_login(user):
    """Given login information, determine whether or not to sign the user in.

    Arguments:
        user {dict} -- Dictionary of login information

    Returns:
        bool -- Whether or not the user is signed in.
    """
    user_data = get_account(user['username'])

    if not user_data:
        flash("Account not found", category="warning")
        return False  # <--- No data at all
    elif user_data.get('pending_verification') == 1:
        flash("This account hasn't been verified. Check your email.")
        return False # <--- The account hasn't been verified yet.
    elif check_password_hash(user_data.get('hashed_password'), user['password']):
        return True  # <--- User is logged in.

    else:
        flash("Incorrect password.")
        return False  # <--- Something else has gone wrong, probably wrong password.

# TODO: Find a way to encrypt user data.

def get_current_access(username):
    """Determine what pages a given user has access to.

    Arguments:
        username {str} -- The user to check

    Returns:
        list -- A list of places the user has permission to view.
    """
    user_data = get_account(username)
    return user_data["have_access_to"].split(',')

# These codes are a joke to brute force. DO NOT USE.
#def check_code(code):
#    """DEPRECIATED. DO NOT USE.
#
#    Arguments:
#        code {code} -- The code to check
#
#    Returns:
#        bool -- Whether or not the code is valid.
#    """
#    with open('text/validcodes.txt', 'r') as file:
#        valid_codes = file.readline()
#
#    if code in valid_codes:
#        code_validity = True
#    else:
#        code_validity = False
#    new_code = str(random.randint(10000, 99999))
#    valid_codes = valid_codes.replace(code, new_code)
#    with open('text/validcodes.txt', 'w') as file:
#        file.write(valid_codes)
#    return code_validity


def update_pw(current_username, new_plain_password):
    """Update a users password.

    Arguments:
        current_username {str} -- The username
        new_plain_password {str} -- The new password, in plaintext.
    """
    # Update database.
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
    #Update UNIX user.
    subprocess.call(shlex.split(
        "sudo sh ./change_pw.sh {} {}".format(current_username, new_plain_password)))

def change_email(username, email, email_type):
    """Change a user's email address.

    Arguments:
        username {str} -- The user to modify.
        email {str} -- The new email address.
        email_type {str} -- Whether the email is a recover_email or a prayer_email.
    """
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    with conn:
        cur.execute("""UPDATE accounts SET {email_type}='{email}' WHERE username='{username}'""".format(
            email_type=email_type, email=email, username=username))

# Checks if user has to a specific area.
# Used by @login_required decorator.

#Everyone has access to writer now.
# def have_access_to_writer(username):
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
