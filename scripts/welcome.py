import time
import platform


import os
from flask import *
from flask_simplelogin import get_username
from werkzeug.security import generate_password_hash, check_password_hash

from account_management import get_account, update_pw, create_account, delete_account

welcome = Blueprint("welcome", __name__)

welcome.route("/")
def welcome_page():
    if platform.node() == "backup-server-vm":
        flash(
            "The main jforseth.tech server is currently experiencing issues. Some functionality may not be available."
        )
    return render_template("welcome/welcome.html")


@welcome.route("/FlaskApp")
def flaskapp_welcome():
    return redirect("/")

@welcome.route("/ifttt")
def ifttt():
    command = request.args.get("command")
    command = command.replace(" ","")
    command = command.lower()
    commands = {
        "prepareforbattle": ["firefox &","konsole &","nohup spotify &"]
    }
    actual_commands = commands.get(command, "echo Invalid Command:{}".format(command))

    os.system('ssh justin@192.168.1.3 "export DISPLAY=:0;' + " ;".join(actual_commands) + '"')
    print('ssh justin@192.168.1.3 "export DISPLAY=:0;' + "; ".join(actual_commands) + '"')
    return ""

@welcome.route("/instructions")
def instructions():
    return render_template("welcome/instructions.html")


@welcome.route("/sign/edit")
def sign_edit():
    with open("text/sign_text.txt") as file:
        text = file.read()
    return render_template("welcome/sign_edit.html", text=text)


@welcome.route("/sign")
def sign():
    return render_template("welcome/sign.html")


@welcome.route("/sign/stream")
def sign_stream():
    def eventStream():
        old_current_number = ""
        while True:
            time.sleep(0.1)
            with open("text/sign_text.txt", "r") as file:
                current_number = file.readline()
            if old_current_number != current_number:
                old_current_number = current_number
                yield "data: {}\n\n".format(current_number)

    return Response(eventStream(), mimetype="text/event-stream")


@welcome.route("/sign/update")
def sign_update():
    text = escape(request.args.get("text"))
    with open("text/sign_text.txt", "w") as file:
        file.write(text)
    return ""


# Random redirects
@welcome.route("/italypics")
def italypics():
    return redirect("https://photos.app.goo.gl/ouxubTRRHkEVnpbr5")

# Old project? Try switching to a "music jeopardy" branch?
@welcome.route("/jeopardy")
def jeopardy():
    return redirect("http://192.168.1.3:5000/jeopardy/buzzer")

@welcome.route("/startpage")
def startpage():
    return redirect("/static/startpages/Evening-Startpage/index.html")
