# -*- coding: utf-8 -*-
import os
import random
import string

from flask import (Flask, flash, redirect, render_template, request,
                   send_from_directory, url_for)
from flask_simplelogin import SimpleLogin, get_username, login_required
from werkzeug.utils import secure_filename

import db_tools
from account_management import (check_my_users, have_access_to_admin,
                                have_access_to_pickem, have_access_to_todo)
from SensitiveData import *
from simple_mail import send_email

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = ['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','py']

app = Flask(__name__)
app.config['SECRET_KEY'] = secretkey
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
SimpleLogin(app, login_checker=check_my_users)

#########
#Welcome#
#########


def welcome():
    # Serves the basic pages for jforseth.tech. No heavy lifting serverside.

    # Home
    @app.route('/')
    def welcomepage():
        return render_template('welcome.html')

    # In case an old link is used.
    @app.route('/FlaskApp')
    def home():
        return redirect('/')

    # The videos page
    @app.route('/videos')
    def videos():
        #A function from chrisalbon.com to break the list apart
        def breaklist(listtobreak, chunksize):
            # For item i in a range that is a length of l,
            for i in range(0, len(listtobreak), chunksize):
                # Create an index range for l of n items:
                yield listtobreak[i:i+chunksize]
        with open("text/videos.txt", 'r') as file:
            videos = file.readlines()
        videos = [i.split('|') for i in videos]
        #mylist=[("Hello", "I hope this works"),("Hi", "I hope this works",),("Hey there", "I hope this works"),("I really hope this works","Hi")]
        videomasterlist=list(breaklist(videos,3))
        return render_template('videos.html', videomasterlist=videomasterlist)

    # About
    @app.route('/about')
    def about():
        return render_template('about.html')
    #Instructions
    @app.route('/instructions')
    def instructions():
        return render_template('instructions.html')
    # Menu
    @app.route('/menu')
    def menu():
        return render_template('menu.html')
###########
#Messenger#
###########


def messenger():
    # Main page
    @app.route('/messenger')
    def messenger_main():
        messages = db_tools.read_messages()
        messages = [''.join(i) for i in messages]
        return render_template("messenger_main.html", result=messages)

    # Shouldn't be necessary any more...
    # iframe with messages
    # @app.route('/messenger/frame')
    # def messenger_frame():
    #    messages = db_tools.read_messages()
    #    messages = [''.join(i) for i in messages]
    #    return render_template("messenger_frame.html", result=messages)

    # New messages
    @app.route('/messenger/result', methods=['POST', 'GET'])
    def result():
        if request.method == 'POST':
            message = request.form.get('Data')
            db_tools.add_message(message)
        return redirect('/messenger')

    # Clear messages
    @app.route('/messenger/clear', methods=['POST', 'GET'])
    def clear():
        db_tools.clear_messages()
        return redirect('/messenger')

########
#Prayer#
########


def prayer():
    # The main page
    @app.route('/prayer')
    def prayerpage():
        return render_template('prayer.html')

    @app.route('/FlaskApp/prayer')
    def oldprayerpage():
        return redirect('/prayer')

    # Email submissions
    @app.route('/prayer/newemail', methods=['POST', 'GET'])
    def new_email():
        if request.method == 'POST':
            email = request.form.get('email')
            parish = request.form.get('parish')
            parish = parish.upper()

            # This is a dictionary that converts the code the user typed in into a parish.
            # REMEMBER TO UPDATE THE HTML
            parish_dictionary = {
                'STJOHNRE': 'Saint John RE',
                'STJOHN': 'Saint John Parish',
                'STJOSEPH': 'Saint Joseph Parish',
                'STJOSEPHRE': 'Saint Joseph RE',
                'FFTEACHERS': 'Fairfield Catholic Teachers',
                'JESUS': 'LL Small Group 3'
            }

            # Takes the parish code, looks it up in the dictionary.
            # If it's blank or incorrect, replace with "Public"
            email_parish = parish_dictionary.get(parish, "Public")
            valid_code = db_tools.get_verification_code()
            message = db_tools.get_verification_email_template()
            message = message.format(
                email_parish, valid_code, email, email_parish)

            # Sends the adapted message
            send_email(
                email, "Thank you for joining JMJprayerrequests", message, projectemail, projectpassword)
            # Displays a page with further instruction
            return render_template('email_adding.html')

    # The second step of verification
    @app.route('/prayer/newemailconfirmed')
    def new_email_confirmed():
        code = request.args.get('code')
        address = request.args.get('email')
        parish = request.args.get('parish')
        try:
            verification_result = db_tools.check_verification_code(code)
        except TypeError:
            "Verification Failed. Your email client may not be supported. Try a different client, e.g. Outlook, your email provider's website, the mail app on your phone, etc."
        if verification_result:  # If verification succeeds:
            # Adds email to applicable groups
            db_tools.add_to_mailing_list(address, parish)
            db_tools.add_to_mailing_list(address, "Public")
            if "RE" in parish:
                new_parish = parish.replace('RE', 'Parish')
                db_tools.add_to_mailing_list(address, new_parish)

            # Returns success page.
            return render_template('email_added.html')
        else:
            # Returns failure message.
            return 'Verification Failed. Please try again.'

    # Prayer request submissions
    @app.route('/prayer/prayerrequest', methods=['POST', 'GET'])
    def prayer_request():
        name = request.form.get('name')
        prequest = request.form.get('prequest')
        parish = request.form.get('parish')

        emails = db_tools.get_emails_from_parish(parish)
        message_template, subject_template = db_tools.read_prayer_request_template(
            name, prequest, parish)

        # For testing purposes only, manually overrides email list and sends to my personal account instead:
        # emails=[personalemail]

        for email in emails:
            send_email(email, subject_template, message_template,
                       projectemail, projectpassword)
        return render_template('sent.html')

######
#TODO#
######


def todo():
    # The main page
    @app.route('/todo')
    @login_required(must=have_access_to_todo)
    def todo_page():
        todos = db_tools.get_todos()
        todos = [i.replace('\n', '') for i in todos]
        todos = [i.replace('COMMA', ',') for i in todos]
        todos.reverse()
        return render_template('todo2.html', result=todos)

    # Submission route for new todos.
    @app.route('/todo/submitted', methods=['POST', 'GET'])
    @login_required(must=have_access_to_todo)
    def answer_submitted():
        name = request.form.get('taskname')
        name = name.replace(',', 'COMMA')
        db_tools.add_todo(name)
        send_email('todo+19z1n4ovd3rf@mail.ticktick.com', name, 'Submitted from jforseth.tech',
                   personalemail, personalpassword)

        return redirect('/todo')

    # Deletion route
    @app.route('/todo/delete', methods=['POST', 'GET'])
    @login_required(must=have_access_to_todo)
    def todo_deleted():
        try:
            taskid = int(request.form.get('taskid'))
        except ValueError:
            return 'Please enter a number...'
        db_tools.delete_todo(taskid)
        return redirect('/todo')

    # Ordering route
    @app.route('/todo/reorder', methods=['POST', 'GET'])
    @login_required(must=have_access_to_todo)
    def todo_reordered():
        try:
            item_to_reorder = int(request.form.get("taskid"))
            position_to_move = int(request.form.get("taskloc"))
        except ValueError:
            return 'Please enter a number...'
        db_tools.reorder_todo(item_to_reorder, position_to_move)
        return redirect('/todo')

##########################
#Farm Year Video Redirect#
##########################


def farmYearVideo():
    @app.route('/FarmYearVideo')
    def FarmYearVideoPage():
        return render_template('FarmYearVideo.html')

    @app.route('/farmyearvideo')
    def FarmYearVideoPage1():
        return render_template('FarmYearVideo.html')

    @app.route('/farm_year_video')
    def FarmYearVideoPage2():
        return render_template('FarmYearVideo.html')

    @app.route('/Farm_Year_Video')
    def FarmYearVideoPage3():
        return render_template('FarmYearVideo.html')

    @app.route('/FARMYEARVIDEO')
    def FarmYearVideoPage4():
        return render_template('FarmYearVideo.html')

    @app.route('/FARM_YEAR_VIDEO')
    def FarmYearVideoPage5():
        return render_template('FarmYearVideo.html')

###########
#Quickdraw#
###########


def quickdrawGame():
    @app.route('/quickdraw')
    @login_required()
    def quickdraw():
        return render_template('quickdraw_client.html')

    @app.route('/quickdraw/shot')
    def quickdraw_shot():
        user = request.args.get('user')
        file = open('text/locked.txt')
        result = file.readlines()
        file.close()
        if result[0] != "True\n":
            file = open('text/locked.txt', 'w')
            file.writelines('True\n'+user)
            file.close()
            return "You were fastest!"
        else:
            return "You were shot by: {}".format(result[1])

    @app.route('/quickdraw/bigscreen')
    def bigscreen():
        return render_template('bigscreen.html')

    @app.route('/quickdraw/bigscreen/begin')
    def bigscreen_begin():
        if random.randint(1, 30) == 1:
            file = open('text/locked.txt', 'w')
            file.write('False')
            file.close()
            return render_template('bigscreen_begin.html', time="1000", result='GO!')
        else:
            file = open('text/locked.txt', 'w')
            file.write('True\nShooting too soon')
            file.close()
            return render_template('bigscreen_begin.html', time='1', result='Not yet')

##############
#Bull Judging#
##############


def bullJudging():
    @app.route('/bulljudging')
    def BullJudgingHomepage():
        return render_template("bulljudginghome.html")

    @app.route('/bulljudging1')
    def BullJudging1():
        return render_template("bulljudging1.html")

    @app.route('/bulljudging2')
    def BullJudging2():
        return render_template("bulljudging2.html")

    @app.route('/bulljudging3')
    def BullJudging3():
        return render_template("bulljudging3.html")

    @app.route('/bulljudging4')
    def BullJudging4():
        return render_template("bulljudging4.html")

    @app.route('/bulljudgingdone')
    def BullJudgingdone():
        return render_template("bulljudgingdone.html")
#######
#Admin#
#######


def admin():
    @app.route('/DBbrowser')
    @login_required(must=have_access_to_admin)
    def DBbrowser():
        messages = db_tools.get_all_from_table("messages")
        accounts = db_tools.get_all_from_table("accounts")
        users = db_tools.get_all_from_table("users")
        return "Messages: <br />{}<br />Accounts:<br />{}<br />Users:<br />{}<br />".format(messages, accounts, users)

##############
#File Sharing#
##############


def file_sharing():
    # This is a magic function from the flask documentation. I have no idea what it does or how it works.
    def allowed_file(filename):
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    @app.route('/filesharing', methods=['GET', 'POST'])
    def upload_file():
        if request.method == "POST":
            if 'file' not in request.files:
                print('No file part')
                return redirect(request.url)
            file = request.files['file']
            if file.filename == '':
                print('No selected file')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                return redirect(url_for('uploaded_file', filename=filename))
        else:    
            filelist=os.listdir(app.config['UPLOAD_FOLDER'])
            return render_template('file_sharing.html',files=filelist)
    @app.route('/filesharing/<filename>')
    def uploaded_file(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'],
                                   filename)
    @app.route('/filesharing/filelist')
    def filelist():
        files=os.listdir(app.config['UPLOAD_FOLDER'])
        return ''.join(files)
######
#Misc#
######
@app.route('/barrelracing')
def barrel_racing():
    return render_template('AP Create Task/index.html')


def scattergories():
    @app.route('/scattergories')
    def scattergories_page():
        file = open(
            r"text/currentcatergorylist.txt")
        catlist = file.readlines()
        file.close()
        catlist = [i.replace('\n', '') for i in catlist]
        file = open(r"text/scattergoriescurrentletter.txt")
        currentletter = file.read()
        file.close()
        return render_template("Scattergories.html", list=catlist, currentletter=currentletter)

    @app.route('/scattergories/newlist')
    def scattergories_newlist():
        file = open(
            r"text/allcatergorylist.txt")
        catlist = file.readlines()
        file.close()
        catlist = [i.replace('\n', '').title() for i in catlist]
        newlist = []
        for i in range(12):
            newlist.append(random.choice(catlist))
        file = open(
            r"text/currentcatergorylist.txt", "w")
        file.writelines(["%s\n" % item for item in newlist])
        file.close()
        return "Done"

    @app.route('/scattergories/roll')
    def scattergories_roll():
        letters = string.ascii_uppercase
        letter = random.choice(letters)
        file = open(r"text/scattergoriescurrentletter.txt", "w")
        file.write(letter)
        file.close()
        return "Done!"
        # Running all of the above
################
#Error Handlers#
################


def errorHandlers():
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    @app.errorhandler(403)
    def forbidden(e):
        return render_template('403.html'), 403

    @app.errorhandler(500)
    def server_error(e):
        return render_template('500.html'), 500


welcome()
messenger()
prayer()
todo()
farmYearVideo()
admin()
errorHandlers()
#bullJudging()
file_sharing()
#scattergories()
#quickdrawGame()

# Runs the testing server.
if __name__ == "__main__":
    app.debug = True
    app.run()
