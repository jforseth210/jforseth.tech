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
    with open("/var/www/jforseth.tech/text/locked.txt") as file:
        result = file.readlines()
    if result[0] == "True\n":
        return "You were shot by: {}".format(result[1])

    with open("/var/www/jforseth.tech/text/locked.txt", "w") as file:
        file.writelines("True\n" + user)
    return "You were fastest!"


@quickdraw_game.route("/quickdraw/bigscreen")
def big_screen():
    return render_template("quickdraw/bigscreen.html")


@quickdraw_game.route("/quickdraw/bigscreen/begin")
def big_screen_begin():
    if random.randint(1, 30) == 1:
        with open("/var/www/jforseth.tech/text/locked.txt", "w") as file:
            file.write("False")
        return render_template(
            "quickdraw/bigscreen_begin.html", time="1000", result="GO!"
        )
    else:
        with open("/var/www/jforseth.tech/text/locked.txt", "w") as file:
            file.write("True\nShooting too soon")
        return render_template(
            "quickdraw/bigscreen_begin.html", time="1", result="Not yet"
        )
