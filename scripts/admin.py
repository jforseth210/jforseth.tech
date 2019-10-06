from flask import *
import db_tools
from flask_simplelogin import login_required
from account_management import have_access_to_admin
admin=Blueprint("admin", __name__)

@admin.route('/DBbrowser')
@login_required(must=have_access_to_admin)
def database_browser():
    messages = db_tools.get_all_from_table("messages")
    accounts = db_tools.get_all_from_table("accounts")
    users = db_tools.get_all_from_table("users")
    return "Messages: <br />{}<br />Accounts:<br />{}<br />Users:<br />{}<br />".format(messages, accounts, users)
