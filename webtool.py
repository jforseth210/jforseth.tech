# -*- coding: utf-8 -*-
from flask import *
from flask_simplelogin import SimpleLogin
from account_management import check_login

from scripts.welcome import *
from scripts.videos import *
from scripts.messenger import *
from scripts.prayer import *
from scripts.todo import *
from scripts.quickdraw_game import *
from scripts.bull_judging import *
from scripts.http_forwarding import *
from scripts.admin import *
from scripts.barrel_racing import *
from scripts.file_sharing import *
# Create the website
app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY


# Account management
SimpleLogin(app, login_checker=check_login)


# __        __   _
# \ \      / /__| | ___ ___  _ __ ___   ___
#  \ \ /\ / / _ \ |/ __/ _ \| '_ ` _ \ / _ \
#   \ V  V /  __/ | (_| (_) | | | | | |  __/
#    \_/\_/ \___|_|\___\___/|_| |_| |_|\___|
# Contains:
# /
# /FlaskApp
# /about
# /instructions
# /menu
app.register_blueprint(welcome)


# __     ___     _
# \ \   / (_) __| | ___  ___  ___
#  \ \ / /| |/ _` |/ _ \/ _ \/ __|
#   \ V / | | (_| |  __/ (_) \__ \
#    \_/  |_|\__,_|\___|\___/|___/
# Contains:
# /videos
# /videos/newupload
# /videos/deletion
# /videos/rename
# /videos/updateid
# /videos/move
app.register_blueprint(videos)


#  __  __
# |  \/  | ___  ___ ___  ___ _ __   __ _  ___ _ __
# | |\/| |/ _ \/ __/ __|/ _ \ '_ \ / _` |/ _ \ '__|
# | |  | |  __/\__ \__ \  __/ | | | (_| |  __/ |
# |_|  |_|\___||___/___/\___|_| |_|\__, |\___|_|
# Contains:                        |___/
# /messenger
# /messenger/result
# /message/stream
# /messenger/clear
app.register_blueprint(messenger)


#  ____
# |  _ \ _ __ __ _ _   _  ___ _ __
# | |_) | '__/ _` | | | |/ _ \ '__|
# |  __/| | | (_| | |_| |  __/ |
# |_|   |_|  \__,_|\__, |\___|_|
# Contains         |___/
# /prayer
# /FlaskApp/prayer
# /prayer/newemail
# /prayer/newemailconfirmed
# /prayer/prayerrequest
app.register_blueprint(prayer)


#  _____         _
# |_   _|__   __| | ___
#   | |/ _ \ / _` |/ _ \
#   | | (_) | (_| | (_) |
#   |_|\___/ \__,_|\___/
# Contains:
# /todolocal
# /todo/submitted
# /todo/delete
# /todo/reorder
app.register_blueprint(todo)


#   ___        _      _       _
#  / _ \ _   _(_) ___| | ____| |_ __ __ ___      __
# | | | | | | | |/ __| |/ / _` | '__/ _` \ \ /\ / /
# | |_| | |_| | | (__|   < (_| | | | (_| |\ V  V /
#  \__\_\\__,_|_|\___|_|\_\__,_|_|  \__,_| \_/\_/
# Contains:
# /quickdraw
# /quickdraw/shot
# /quickdraw/bigscreen
# /quickdraw/bigscreen/begin
app.register_blueprint(quickdraw_game)


#  ____        _ _       _           _       _
# | __ ) _   _| | |     | |_   _  __| | __ _(_)_ __   __ _
# |  _ \| | | | | |  _  | | | | |/ _` |/ _` | | '_ \ / _` |
# | |_) | |_| | | | | |_| | |_| | (_| | (_| | | | | | (_| |
# |____/ \__,_|_|_|  \___/ \__,_|\__,_|\__, |_|_| |_|\__, |
# Contains:                             |___/         |___/
# /bulljudging
# /bulljudging1
# /bulljudging2
# /bulljudging3
# /bulljudging4
# /bulljudgingdone
app.register_blueprint(bull_judging)


#     _       _           _
#    / \   __| |_ __ ___ (_)_ __
#   / _ \ / _` | '_ ` _ \| | '_ \
#  / ___ \ (_| | | | | | | | | | |
# /_/   \_\__,_|_| |_| |_|_|_| |_|
# #Contains:
# /DBbrowser
# app.register_blueprint(admin)


#  ____                      _   ____            _
# | __ )  __ _ _ __ _ __ ___| | |  _ \ __ _  ___(_)_ __   __ _
# |  _ \ / _` | '__| '__/ _ \ | | |_) / _` |/ __| | '_ \ / _` |
# | |_) | (_| | |  | | |  __/ | |  _ < (_| | (__| | | | | (_| |
# |____/ \__,_|_|  |_|  \___|_| |_| \_\__,_|\___|_|_| |_|\__, |
# Contains:                                               |___/
# /barrelracing/app_lab
# /barrelracing/counter
# /barrelracing/counter/currentnumber
# /barrelracing/current_number_update
# /barrelracing/stream
app.register_blueprint(barrel_racing)


#  _____ _ _        ____  _                _
# |  ___(_) | ___  / ___|| |__   __ _ _ __(_)_ __   __ _
# | |_  | | |/ _ \ \___ \| '_ \ / _` | '__| | '_ \ / _` |
# |  _| | | |  __/  ___) | | | | (_| | |  | | | | | (_| |
# |_|   |_|_|\___| |____/|_| |_|\__,_|_|  |_|_| |_|\__, |
# Contains:                                         |___/
# /filesharing
# /filesharing/<filename>
# /filesharing/filelist
app.register_blueprint(file_sharing)


#  _____                       _   _                 _ _
# | ____|_ __ _ __ ___  _ __  | | | | __ _ _ __   __| | | ___ _ __ ___
# |  _| | '__| '__/ _ \| '__| | |_| |/ _` | '_ \ / _` | |/ _ \ '__/ __|
# | |___| |  | | | (_) | |    |  _  | (_| | | | | (_| | |  __/ |  \__ \
# |_____|_|  |_|  \___/|_|    |_| |_|\__,_|_| |_|\__,_|_|\___|_|  |___/
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')


@app.errorhandler(403)
def forbidden(e):
    return render_template('403.html')


@app.errorhandler(500)
def server_error(e):
    return render_template('500.html')


if __name__ == "__main__":
    app.debug = True
    app.run()
