# -*- coding: utf-8 -*-
import subprocess
import platform

from flask import app, Flask, render_template
from flask_debugtoolbar import DebugToolbarExtension
from flask_simplelogin import SimpleLogin, is_logged_in, get_username

from SensitiveData import SECRET_KEY

from account_management import check_login
from scripts.welcome import welcome
from scripts.accounts import accounts, get_current_access
from scripts.writer import writer
from scripts.videos import videos
from scripts.messenger import messenger
from scripts.prayer import prayer
from scripts.lucky_shoe import lucky_shoe
from scripts.todo import todo
from scripts.scattergories import scattergories
from scripts.quickdraw_game import quickdraw_game
from scripts.bull_judging import bull_judging
from scripts.http_forwarding import http_forwarding
from scripts.admin import admin
from scripts.barrel_racing import barrel_racing
from scripts.file_sharing import file_sharing
from scripts.LQA import LQA

app = Flask(__name__)
app.config["SECRET_KEY"] = SECRET_KEY

messages = {
    "login_success": "Login Successful",
    "login_failure": "Something went wrong. Dismiss this banner to learn more.",
    "is_logged_in": "You're already logged in!",
    "logout": "Logout Successful",
    "login_required": "You need to sign in to use this feature.",
    "access_denied": "Access Denied",
    "auth_error": "{0}",
}

# Account management
SimpleLogin(app, login_checker=check_login, messages=messages)


def check_if_admin():
    """Check if a given user has admin access.

    Returns:
        bool -- Whether or not the user has admin access.
    """
    return bool(is_logged_in() and 'admin' in get_current_access(get_username()))


app.jinja_env.globals.update(check_if_admin=check_if_admin)

# __        __   _
# \ \      / /__| | ___ ___  _ __ ___   ___
#  \ \ /\ / / _ \ |/ __/ _ \| '_ ` _ \ / _ \
#   \ V  V /  __/ | (_| (_) | | | | | |  __/
#    \_/\_/ \___|_|\___\___/|_| |_| |_|\___|
app.register_blueprint(welcome)


#    _                         _
#   / \   ___ ___  _   _ _ __ | |_ ___
#  / _ \ / __/ _ \| | | | '_ \| __/ __|
# / ___ \ (_| (_) | |_| | | | | |_\__ \
# /_/   \_\___\___/ \__,_|_| |_|\__|___/
app.register_blueprint(accounts)

# __     ___     _
# \ \   / (_) __| | ___  ___  ___
#  \ \ / /| |/ _` |/ _ \/ _ \/ __|
#   \ V / | | (_| |  __/ (_) \__ \
#    \_/  |_|\__,_|\___|\___/|___/
app.register_blueprint(videos)


#  __  __
# |  \/  | ___  ___ ___  ___ _ __   __ _  ___ _ __
# | |\/| |/ _ \/ __/ __|/ _ \ '_ \ / _` |/ _ \ '__|
# | |  | |  __/\__ \__ \  __/ | | | (_| |  __/ |
# |_|  |_|\___||___/___/\___|_| |_|\__, |\___|_|
#                                  |___/
#app.register_blueprint(messenger)


#  ____
# |  _ \ _ __ __ _ _   _  ___ _ __
# | |_) | '__/ _` | | | |/ _ \ '__|
# |  __/| | | (_| | |_| |  __/ |
# |_|   |_|  \__,_|\__, |\___|_|
#                  |___/
app.register_blueprint(prayer)


# __        __    _ _
# \ \      / / __(_) |_ ___ _ __
# \ \ /\ / / '__| | __/ _ \ '__|
#  \ V  V /| |  | | ||  __/ |
#   \_/\_/ |_|  |_|\__\___|_|
app.register_blueprint(writer)


# _               _            ____  _
# | |   _   _  ___| | ___   _  / ___|| |__   ___   ___
# | |  | | | |/ __| |/ / | | | \___ \| '_ \ / _ \ / _ \
# | |__| |_| | (__|   <| |_| |  ___) | | | | (_) |  __/
# |_____\__,_|\___|_|\_\\__, | |____/|_| |_|\___/ \___|
#                       |___/
#app.register_blueprint(lucky_shoe)


#  _____         _
# |_   _|__   __| | ___
#   | |/ _ \ / _` |/ _ \
#   | | (_) | (_| | (_) |
#   |_|\___/ \__,_|\___/
#app.register_blueprint(todo)


# ____            _   _                            _
# / ___|  ___ __ _| |_| |_ ___ _ __ __ _  ___  _ __(_) ___  ___
# \___ \ / __/ _` | __| __/ _ \ '__/ _` |/ _ \| '__| |/ _ \/ __|
# ___) | (_| (_| | |_| ||  __/ | | (_| | (_) | |  | |  __/\__ \
# |____/ \___\__,_|\__|\__\___|_|  \__, |\___/|_|  |_|\___||___/
#app.register_blueprint(scattergories)


#   ___        _      _       _
#  / _ \ _   _(_) ___| | ____| |_ __ __ ___      __
# | | | | | | | |/ __| |/ / _` | '__/ _` \ \ /\ / /
# | |_| | |_| | | (__|   < (_| | | | (_| |\ V  V /
#  \__\_\\__,_|_|\___|_|\_\__,_|_|  \__,_| \_/\_/
#app.register_blueprint(quickdraw_game)


#  ____        _ _       _           _       _
# | __ ) _   _| | |     | |_   _  __| | __ _(_)_ __   __ _
# |  _ \| | | | | |  _  | | | | |/ _` |/ _` | | '_ \ / _` |
# | |_) | |_| | | | | |_| | |_| | (_| | (_| | | | | | (_| |
# |____/ \__,_|_|_|  \___/ \__,_|\__,_|\__, |_|_| |_|\__, |
#                                       |___/         |___/
#app.register_blueprint(bull_judging)


#     _       _           _
#    / \   __| |_ __ ___ (_)_ __
#   / _ \ / _` | '_ ` _ \| | '_ \
#  / ___ \ (_| | | | | | | | | | |
# /_/   \_\__,_|_| |_| |_|_|_| |_|
#app.register_blueprint(admin)
#app.register_blueprint(http_forwarding)

#  ____                      _   ____            _
# | __ )  __ _ _ __ _ __ ___| | |  _ \ __ _  ___(_)_ __   __ _
# |  _ \ / _` | '__| '__/ _ \ | | |_) / _` |/ __| | '_ \ / _` |
# | |_) | (_| | |  | | |  __/ | |  _ < (_| | (__| | | | | (_| |
# |____/ \__,_|_|  |_|  \___|_| |_| \_\__,_|\___|_|_| |_|\__, |
#app.register_blueprint(barrel_racing)


#  _____ _ _        ____  _                _
# |  ___(_) | ___  / ___|| |__   __ _ _ __(_)_ __   __ _
# | |_  | | |/ _ \ \___ \| '_ \ / _` | '__| | '_ \ / _` |
# |  _| | | |  __/  ___) | | | | (_| | |  | | | | | (_| |
# |_|   |_|_|\___| |____/|_| |_|\__,_|_|  |_|_| |_|\__, |
#app.register_blueprint(file_sharing)


# _     ___      _
# | |   / _ \    / \
# | |  | | | |  / _ \
# | |__| |_| | / ___ \
# |_____\__\_\/_/   \_\
#app.register_blueprint(LQA)


#  _____                       _   _                 _ _
# | ____|_ __ _ __ ___  _ __  | | | | __ _ _ __   __| | | ___ _ __ ___
# |  _| | '__| '__/ _ \| '__| | |_| |/ _` | '_ \ / _` | |/ _ \ '__/ __|
# | |___| |  | | | (_) | |    |  _  | (_| | | | | (_| | |  __/ |  \__ \
# |_____|_|  |_|  \___/|_|    |_| |_|\__,_|_| |_|\__,_|_|\___|_|  |___/
@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404


@app.errorhandler(403)
def forbidden(e):
    return render_template('errors/403.html'), 403


@app.errorhandler(500)
def server_error(e):
    # if not app.debug:
    #     send_email('support@jforseth.tech', 'It\'s reprogramming time!',
    #                "<a href=\"https://youtu.be/QDSEpjjavhY?t=182\">It's reprogramming time!</a><br/>An error was detected on your server: {}".format(e),
    #                'errors@jforseth.tech', PROJECT_PASSWORD)
    return render_template("errors/500.html"), 500


if __name__ == "__main__":
    app.debug = True
    # toolbar=DebugToolbarExtension(app)
    app.run(host="0.0.0.0")
