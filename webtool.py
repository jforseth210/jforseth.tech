# -*- coding: utf-8 -*-
from simple_mail import send_email
from SensitiveData import *
from account_management import (check_my_users, have_access_to_admin,
                                have_access_to_pickem, have_access_to_todo)
import db_tools
from werkzeug.utils import secure_filename
from flask_simplelogin import SimpleLogin, get_username, login_required
from flask import (Flask, flash, redirect, render_template, request,
                   send_from_directory, url_for)
import os
import random
import string
import pprint
pp = pprint.PrettyPrinter(indent=4)


UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = ['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'py']

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

    # About
    @app.route('/about')
    def about():
        return render_template('about.html')
    # Instructions
    @app.route('/instructions')
    def instructions():
        return render_template('instructions.html')
    # Menu
    @app.route('/menu')
    def menu():
        return render_template('menu.html')
########
#Videos#
########
    # This route is for loading the video page.
    # If the user is signed in as admin, the admin tools will show,
    # if not, only the default video page will be sent. See videos.html
    # for more info.
    @app.route('/videos')
    def videos():

        # A function from chrisalbon.com to break the list apart
        # This function is used to break the video list into rows.
        def breaklist(listtobreak, chunksize):
            # For item i in a range that is a length of l,
            for i in range(0, len(listtobreak), chunksize):
                # Create an index range for l of n items:
                yield listtobreak[i:i+chunksize]

        # videos.txt is the list of videos
        # It's formatted like this:
        #   The video's title|YoutubeID
        #   Another video|YoutubeID
        # Note that the youtube id is not the same as the link to the video.
        with open("text/videos.txt", 'r') as file:
            videos = file.readlines()
        # As always, newlines make a mess.
        # In this case, it breaks some of the admin tools further down break.
        videos = [i.replace(' \n', '') for i in videos]

        # Split videos into a list of sublists, each with two items, the title and the id.
        # So:
        # [['title','youtubeid'],['title','youtubeid']]
        videos = [i.split('|') for i in videos]

        # This list is then broken into chunks of three to form rows:
        # [
        #   [
        #       [video0,video0id],
        #       [video1,video1id],
        #       [video2,video2id]
        #   ],
        #   [
        #       [video3,video3id],
        #       [video4,video4id],
        #       [video5,video5id]
        #   ]
        # ]
        # Note, if you want to change the number of videos per row, update the '3' below
        # Just make sure you modify the corresponding css.
        # In hindsight this all probably could've been done using some clever css.
        # Oh well, I'm not clever in css. I'm clever in python.
        videomasterlist = list(breaklist(videos, 3))
        return render_template('videos.html', videomasterlist=videomasterlist)

    # The upload form sends its data here.
    @app.route('/videos/newupload', methods=["POST"])
    @login_required(must=have_access_to_admin)
    def newupload():
        # Title is the title to be shown on jforseth.tech, not the title on youtube.
        title = request.form.get('title')
        # This is the link to the video, not the id.
        # Playlists and youtu.be links are hit or miss.
        youtubeid = request.form.get('youtubeid')

        # If there are any seperators, delete them, they'll break things later.
        title = title.replace('|', '')

        # If the link the user uploaded isn't a youtube link, let them know.
        if 'https://www.youtube.com/watch?v=' not in youtubeid and 'https://youtu.be/' not in youtubeid:
            return "This doesn't look like a YouTube link. Try again."

        # Remove the url part, all we care about is the video id.
        youtubeid = youtubeid.replace('https://www.youtube.com/watch?v=', '')
        youtubeid = youtubeid.replace('https://youtu.be/', '')

        # Get the existing video list.
        with open('text/videos.txt', 'r') as file:
            vidlist = file.readlines()

        # Take the title and id of the new video and format it for the list.
        newvideo = title+'|'+youtubeid+'\n'

        # Insert it at the top of the list
        vidlist.insert(0, newvideo)

        # Write the updated list to the file.
        with open('text/videos.txt', 'w') as file:
            file.writelines(vidlist)

        # Return to the video page.
        return redirect('../videos')

    # The delete button sends the video id it wants deleted here.
    @app.route('/videos/deletion', methods=["POST"])
    @login_required(must=have_access_to_admin)
    def deletion():

        # This is the id of the youtube video to delete.
        # It is not a URL!
        youtubeid = request.form.get('youtubeid')

        # Read the list of videos.
        with open('text/videos.txt', 'r') as file:
            vidlist = file.readlines()

        # This magical line removes videos that have the link requested for deletion.
        # It iterates through the list of videos, discarding any that element with the id that is to be deleted.
        # Note: A malicious request containing only one character may delete multiple videos.
        # MAKE SURE ALL ADMINS ARE TRUSTED.
        vidlist = [v for v in vidlist if youtubeid not in v]

        # Finally, it overwrites the old list.
        with open('text/videos.txt', 'w') as file:
            file.writelines(vidlist)
        return redirect('../videos')

    # The video rename form sends its data here.
    @app.route('/videos/rename', methods=["POST"])
    @login_required(must=have_access_to_admin)
    def rename():

        # New title of renamed video
        title = request.form.get('title')

        # This is the id of the youtube video to delete.
        # It is not a URL!
        youtubeid = request.form.get('youtubeid')

        # Again, reads the list of videos.
        with open('text/videos.txt', 'r') as file:
            vidlist = file.readlines()

        # List comprehensions didn't seem like a good option.
        vidlist2 = []
        for i in vidlist:

            # Search for the video to be renamed by id.
            if youtubeid in i:
                # Keep the id, throw the old name away.
                _, iyoutubeid = i.split('|')

                # Put new title, old id together, in the proper format.
                vidlist2.append(title+'|'+iyoutubeid)
            else:

                # If its not the video we're looking for, don't do anything.
                vidlist2.append(i)

        # Basically a list comprehension. Replace the old list with the new one.
        vidlist = vidlist2

        # Overwrite the old list.
        with open('text/videos.txt', 'w') as file:
            file.writelines(vidlist)

        # Redirect to video page, should just look like reload.
        return redirect('../videos')

    @app.route('/videos/updateid', methods=["POST"])
    @login_required(must=have_access_to_admin)
    def updateid():

        # Original id of the video.
        oldyoutubeid = request.form.get('oldyoutubeid')
        # New id of the video.
        newyoutubeid = request.form.get('newyoutubeid')

        # If the user sends a link and not an id, quietly delete the parts that don't matter.
        newyoutubeid = newyoutubeid.replace(
            'https://www.youtube.com/watch?v=', '')
        newyoutubeid = newyoutubeid.replace('https://youtu.be/', '')

        # Read the video list.
        with open('text/videos.txt', 'r') as file:
            vidlist = file.readlines()

        # TODO: Make this into a list comprehension.
        # Basically, search for the id you want to replace, replace it, write your changes to a new list.
        vidlist2 = []
        for i in vidlist:
            if oldyoutubeid in i:
                i = i.replace(oldyoutubeid, newyoutubeid)
            vidlist2.append(i)

        # Point the old list to your new one.
        vidlist = vidlist2

        # Overwrite and reload. You know the drill.
        with open('text/videos.txt', 'w') as file:
            file.writelines(vidlist)
        return redirect('../videos')

    # The move up and move down buttons send data here.
    @app.route('/videos/move', methods=["POST"])
    @login_required(must=have_access_to_admin)
    def move():
        # This is the EXACT element in the video list. If its not, it'll cause a ValueError.
        element = request.form.get('element')+'\n'

        # The direction to move the video, 'up' or 'down'
        direction = request.form.get('direction')

        # Again, just reading the video list.
        with open('text/videos.txt', 'r') as file:
            vidlist = file.readlines()

        # Find the index for the desired element.
        videoindex = vidlist.index(element)

        # Remove the element at that position. Without this line,
        # the video will appear twice, both in the old position, and the new one.
        vidlist.pop(videoindex)

        # Now, shift the index by one. 
        if direction == 'up':
            # I know subtracting seems counter-intuitive, but remember, index 0 is the top of the list. 
            videoindex -= 1
        else:
            # The bigger index, the lower on the list. 
            videoindex += 1

        #Insert the element, exactly as it was, in its new position, exactly one higher or one lower. 
        vidlist.insert(videoindex, element)

        #Overwrite and refresh. 
        with open('text/videos.txt', 'w') as file:
            file.writelines(vidlist)
        return redirect('../videos')
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
            filelist = os.listdir(app.config['UPLOAD_FOLDER'])
            return render_template('file_sharing.html', files=filelist)

    @app.route('/filesharing/<filename>')
    def uploaded_file(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'],
                                   filename)

    @app.route('/filesharing/filelist')
    def filelist():
        files = os.listdir(app.config['UPLOAD_FOLDER'])
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
# bullJudging()
file_sharing()
# scattergories()
# quickdrawGame()

# Runs the testing server.
if __name__ == "__main__":
    app.debug = True
    app.run()
