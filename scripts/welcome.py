from flask import *
from account_management import get_account
from flask_simplelogin import get_username
welcome = Blueprint('welcome', __name__)


@welcome.route('/')
def welcome_page():
    return render_template("welcome/welcome.html")


@welcome.route('/FlaskApp')
def flaskapp_welcome():
    return redirect('/')


@welcome.route('/about')
def about():
    return render_template('welcome/about.html')


@welcome.route('/instructions')
def instructions():
    return render_template('welcome/instructions.html')


@welcome.route('/menu')
def menu():
    return render_template('welcome/menu.html')

@welcome.route('/signup')
def signup():
    return render_template('welcome/signup.html')

@welcome.route('/account')
def account():
    account=get_account(get_username())
    account.pop("hashed_password")
    return render_template('welcome/account.html',account=account)