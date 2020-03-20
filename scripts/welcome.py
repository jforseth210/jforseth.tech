import platform
from flask import *
import time
from account_management import get_account, update_pw
from flask_simplelogin import get_username
from werkzeug.security import generate_password_hash, check_password_hash
welcome = Blueprint('welcome', __name__)


@welcome.route('/')
def welcome_page():
    if platform.node()=="backup-server-vm":
         flash("The main jforseth.tech server is currently experiencing issues. Some functionality may not be available.")
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

@welcome.route('/signup')
def signup():
    return render_template('welcome/signup.html')

@welcome.route('/account/<account>')
def account(account):
    if account == get_username():
        account=get_account(get_username())
        account.pop("hashed_password")
        return render_template('welcome/account.html',account=account)
    return render_template("errors/403.html"), 403

@welcome.route('/changepw', methods=["GET","POST"])
def change_password():
    old_password=request.form.get("old_password")
    new_password=request.form.get("new_password")
    current_username=get_username()
    current_account=get_account(current_username)
    if check_password_hash(current_account.get("hashed_password"), old_password):
        new_hashed_password=generate_password_hash(new_password)
        update_pw(current_username, new_hashed_password)
        flash("Success!", category="success")
    else:
        flash("Old password incorrect.", category="warning")
    return redirect("/account/{}".format(current_username))
@welcome.route('/sign/edit')
def sign_edit():
    with open("text/sign_text.txt") as file:
        text=file.read()
    return render_template("welcome/sign_edit.html", text=text)

@welcome.route('/sign')
def sign():
    return render_template("welcome/sign.html")

@welcome.route('/sign/stream')
def sign_stream():
    def eventStream():
        old_current_number=''
        while True:
            time.sleep(0.1)
            with open("text/sign_text.txt", 'r') as file:
                current_number = file.readline()
            if old_current_number != current_number:
                old_current_number = current_number
                yield "data: {}\n\n".format(current_number)
    return Response(eventStream(), mimetype="text/event-stream")
@welcome.route("/sign/update")
def sign_update():
    text=request.args.get("text")
    with open("text/sign_text.txt","w") as file:
        file.write(text)
    return ""
#Random redirects
@welcome.route("/italypics")
def italypics():
    return redirect("https://photos.app.goo.gl/ouxubTRRHkEVnpbr5")

@welcome.route("/jeopardy")
def jeopardy():
    return redirect("http://192.168.1.3:5000/jeopardy/buzzer")
