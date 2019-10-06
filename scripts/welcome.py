from flask import *
welcome=Blueprint('welcome',__name__)

@welcome.route('/')
def welcome_page():
    return render_template("welcome.html")

@welcome.route('/FlaskApp')
def flaskapp_welcome():
    return redirect('/')

@welcome.route('/about')
def about():
    return render_template('about.html')

@welcome.route('/instructions')
def instructions():
    return render_template('instructions.html')

@welcome.route('/menu')
def menu():
    return render_template('menu.html')