import random

from flask import *
from flask_simplelogin import login_required

quickdraw_game = Blueprint("quickdraw_game", __name__)  # Main page


@quickdraw_game.route("/quickdraw")
@login_required()
def quickdraw():
    return render_template("quickdraw/quickdraw_client.html")


@quickdraw_game.route("/quickdraw/shot")
def quickdraw_shot():
    user = escape(request.args.get("user"))
    file = open("text/locked.txt")
    result = file.readlines()
    file.close()
    if result[0] != "True\n":
        file = open("text/locked.txt", "w")
        file.writelines("True\n" + user)
        file.close()
        return "You were fastest!"
    else:
        return "You were shot by: {}".format(result[1])


@quickdraw_game.route("/quickdraw/bigscreen")
def big_screen():
    return render_template("quickdraw/bigscreen.html")


@quickdraw_game.route("/quickdraw/bigscreen/begin")
def big_screen_begin():
    if random.randint(1, 30) == 1:
        file = open("text/locked.txt", "w")
        file.write("False")
        file.close()
        return render_template(
            "quickdraw/bigscreen_begin.html", time="1000", result="GO!"
        )
    else:
        file = open("text/locked.txt", "w")
        file.write("True\nShooting too soon")
        file.close()
        return render_template(
            "quickdraw/bigscreen_begin.html", time="1", result="Not yet"
        )
