# -*- coding: utf-8 -*-
from flask import *
from flask_simplelogin import SimpleLogin
from scripts.account_management import check_my_users

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
SimpleLogin(app, login_checker=check_my_users)

#Contains:
#/httpforwarding
app.register_blueprint(http_forwarding)

#Contains:
#/
#/FlaskApp
#/about
#/instructions
#/menu
app.register_blueprint(welcome)

#Contains:
#/videos
#/videos/newupload
#/videos/deletion
#/videos/rename
#/videos/updateid
#/videos/move
app.register_blueprint(videos)
    
#Contains:
#/messenger
#/messenger/result
#/message/stream
#/messenger/clear
app.register_blueprint(messenger)

#Contains
#/prayer
#/FlaskApp/prayer
#/prayer/newemail
#/prayer/newemailconfirmed
#/prayer/prayerrequest
app.register_blueprint(prayer)

#Contains:
#/todo
#/todo/submitted
#/todo/delete
#/todo/reorder
app.register_blueprint(todo)

#Contains:
#/quickdraw
#/quickdraw/shot
#/quickdraw/bigscreen
#/quickdraw/bigscreen/begin
app.register_blueprint(quickdraw_game)    

#Contains:
#/bulljudging
#/bulljudging1
#/bulljudging2
#/bulljudging3
#/bulljudging4
#/bulljudgingdone
app.register_blueprint(bull_judging)

#Contains:
#/DBbrowser
app.register_blueprint(admin)

#Contains:
#/barrelracing/app_lab
#/barrelracing/counter
#/barrelracing/counter/currentnumber
#/barrelracing/current_number_update
#/barrelracing/stream
app.register_blueprint(barrel_racing)

#Contains:
#/filesharing
#/filesharing/<filename>
#/filesharing/filelist
app.register_blueprint(file_sharing)
#Error handlers
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(403)
def forbidden(e):
    return render_template('403.html'), 403

@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500


if __name__ == "__main__":
    app.debug = True
    app.run()
