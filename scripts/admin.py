import sqlite3
from flask import *
from flask_simplelogin import login_required

from account_management import have_access_to_admin
admin = Blueprint("admin", __name__)

# Dumps the database for anyone with admin access.
# This is a security nightmare! It should NEVER be enabled.


def get_all_from_table(table):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM {}".format(table))
    return cur.fetchall()


@admin.route('/DBbrowser')
@login_required(must=have_access_to_admin)
def database_browser():
    messages = get_all_from_table("messages")
    accounts = get_all_from_table("accounts")
    users = get_all_from_table("users")
    return "Messages: <br />{}<br />Accounts:<br />{}<br />Users:<br />{}<br />".format(messages, accounts, users)


@admin.route('/error')
@login_required(must=have_access_to_admin)
def error_page():
    raise Exception(
        "This exception was deliberately caused. Why did you do that?")
