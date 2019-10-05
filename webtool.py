# -*- coding: utf-8 -*-

# Custom module for sending emails.
from simple_mail import send_email

# Data I don't want on github
from SensitiveData import *

# For integrating flask_simplelogin with my database.
from account_management import (check_my_users, have_access_to_admin,
                                have_access_to_pickem, have_access_to_todo)

# Tools I created for reading/writing data.
# Mostly abstracts open() function and some
# sqlite stuff.
import db_tools

# For filesharing
from werkzeug.utils import secure_filename

# For accounts, mostly just admin account.
from flask_simplelogin import SimpleLogin, get_username, login_required

# The framework that runs all of it.
from flask import (Flask, flash, redirect, render_template, request,
                   send_from_directory, url_for, Response)

# Lists the files in the upload directory.
import os

# Randomness is always useful
import random
import time
# Random letter generator
import string

# Useful for debug.
import pprint
pp = pprint.PrettyPrinter(indent=4)


import requests
#from requests_html import HTMLSession


# From flask docs
UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = ['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'py']


# Create the website. Setup secret_key, upload location, logins.
app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
SimpleLogin(app, login_checker=check_my_users)
@app.route("/experiment")
def experiment():
    requested_url=request.args.get('url')
    if requested_url == None:
        page="Enter your desired page"
    else:
        session=HTMLSession()
        page=session.get(requested_url)
        absolute_links=page.html.absolute_links
        links=page.html.links
        page=page.html.raw_html
        pp.pprint(absolute_links)
        #for i in links:
        #    if i in absolute_links:
        #        page=page.replace(bytes(i,'utf-8'),b"http://jforseth.tech/experiment?url="+bytes(i,'utf-8'))
        #    else:
        #        page=page.replace(bytes(i,'utf-8'),b"http://jforseth.tech/experiment?url="+bytes(requested_url,'utf-8')+bytes(i,'utf-8'))
        ATTRIBUTES=['src','href','content','action']
        requested_url_utf=requested_url.encode('utf-8')
        for i in ATTRIBUTES:
            page=page.replace(b"{}='/",b'src=http://jforseth.tech/experiment?url='+requested_url_utf+b'/').format(i)
            page=page.replace(b'{}=\"/',b'src=http://jforseth.tech/experiment?url='+requested_url_utf+b'/').format(i)
            page=page.replace(b'{}=/',b'src=http://jforseth.tech/experiment?url='+requested_url_utf+b'/').format(i)
        # page=page.replace(b"src='/",b'src=http://jforseth.tech/experiment?url='+requested_url.encode('utf-8')+b'/')
        # page=page.replace(b"href='/",b'href=http://jforseth.tech/experiment?url='+requested_url.encode('utf-8')+b'/')
        # page=page.replace(b"content='/",b'content=http://jforseth.tech/experiment?url='+requested_url.encode('utf-8')+b'/')
        # page=page.replace(b'src=\"/',b'src=http://jforseth.tech/experiment?url='+requested_url.encode('utf-8')+b'/')
        # page=page.replace(b'href=\"/',b'href=http://jforseth.tech/experiment?url='+requested_url.encode('utf-8')+b'/')
        # page=page.replace(b'content=\"/',b'content=http://jforseth.tech/experiment?url='+requested_url.encode('utf-8')+b'/')
        # page=page.replace(b'src=/',b'src=http://jforseth.tech/experiment?url='+requested_url.encode('utf-8')+b'/')
        # page=page.replace(b'href=/',b'href=http://jforseth.tech/experiment?url='+requested_url.encode('utf-8')+b'/')
        # page=page.replace(b'content=/',b'content=http://jforseth.tech/experiment?url='+requested_url.encode('utf-8')+b'/')
    return "<form><input name='url' /><input type='submit'></form>"+str(page)
#########
#Welcome#
#########
# Welcome
#
# Instructions
# Mobile Menubar

def welcome():
    # Serves the basic pages for jforseth.tech. No heavy lifting serverside.

    # Home
    @app.route('/')
    def welcome_page():

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

    # Mobile Menu
    @app.route('/menu')
    def menu():
        return render_template('menu.html')
########
#Videos#
########


def videos():
    # This route is for loading the video page.

    # If the user is signed in as admin, the admin tools will show,
    # if not, only the default video page will be sent. See videos.html
    # for more info.
    @app.route('/videos')
    def video_page():
        # Get the list of videos
        videos = db_tools.get_videos()

        # Remove newlines
        videos = [i.replace(' \n', '') for i in videos]
        # Split videos into a list of sublists, each with two items, the title and the id.
        videos = [i.split('|') for i in videos]

        # A function from chrisalbon.com to break the list into rows
        def break_list(list_to_break, chunk_size):
            for i in range(0, len(list_to_break), chunk_size):

                yield list_to_break[i:i+chunk_size]

        video_master_list = list(break_list(videos, 3))
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

        return render_template('videos.html', video_master_list=video_master_list)

    # The upload form sends its data here.
    @app.route('/videos/newupload', methods=["POST"])
    @login_required(must=have_access_to_admin)
    def new_video_upload():
        # Title is the title to be shown on jforseth.tech, not the title on youtube.
        title = request.form.get('title')
        # This is the link to the video, not the id.
        # Playlists and youtu.be links are hit or miss.
        youtube_id = request.form.get('youtube_id')

        # If there are any seperators, delete them, they'll break things later.
        title = title.replace('|', '')

        # If the link the user uploaded isn't a youtube link, let them know.
        if 'https://www.youtube.com/watch?v=' not in youtube_id and 'https://youtu.be/' not in youtube_id:
            return "This doesn't look like a YouTube link. Try again."

        # Remove the url part, all we care about is the video id.
        youtube_id = youtube_id.replace('https://www.youtube.com/watch?v=', '')
        youtube_id = youtube_id.replace('https://youtu.be/', '')

        # Get the existing video list.
        video_list = db_tools.get_videos()

        # Take the title and id of the new video and format it for the list.
        newvideo = title+'|'+youtube_id+'\n'

        # Insert it at the top of the list
        video_list.insert(0, newvideo)

        # Write the updated list to the file.
        db_tools.overwrite_videos(video_list)

        # Return to the video page.
        return redirect('../videos')

    # The delete button sends the video id it wants deleted here.
    @app.route('/videos/deletion', methods=["POST"])
    @login_required(must=have_access_to_admin)
    def deletion():
        # This is the id of the youtube video to delete.
        # It is not a URL!
        youtube_id = request.form.get('youtube_id')

        # Read the list of videos.
        video_list = db_tools.get_videos()
        if len(youtube_id) < 12:
            return "This doesn't look like a valid youtube link."
        # This magical line removes videos that have the link requested for deletion.
        # It iterates through the list of videos, discarding any that element with the id that is to be deleted.
        # Note: A malicious request containing only one character may delete multiple videos.
        # MAKE SURE ALL ADMINS ARE TRUSTED.
        video_list = [v for v in video_list if youtube_id not in v]

        # Finally, it overwrites the old list.
        db_tools.overwrite_videos(video_list)
        return redirect('../videos')

    # The video rename form sends its data here.
    @app.route('/videos/rename', methods=["POST"])
    @login_required(must=have_access_to_admin)
    def rename():

        # New title of renamed video
        title = request.form.get('title')

        # This is the id of the youtube video to delete.
        # It is not a URL!
        youtube_id = request.form.get('youtube_id')

        # Again, reads the list of videos.
        video_list = db_tools.get_videos()
        # List comprehensions didn't seem like a good option.
        video_list2 = []
        for i in video_list:

            # Search for the video to be renamed by id.
            if youtube_id in i:
                # Keep the id, throw the old name away.
                _, iyoutube_id = i.split('|')

                # Put new title, old id together, in the proper format.
                video_list2.append(title+'|'+iyoutube_id)
            else:

                # If its not the video we're looking for, don't do anything.
                video_list2.append(i)

        # Basically a list comprehension. Replace the old list with the new one.
        video_list = video_list2

        # Overwrite the old list.
        db_tools.overwrite_videos(video_list)
        # Redirect to video page, should just look like reload.
        return redirect('../videos')

    @app.route('/videos/updateid', methods=["POST"])
    @login_required(must=have_access_to_admin)
    def update_video_id():

        # Original id of the video.
        old_youtube_id = request.form.get('old_youtube_id')
        # New id of the video.
        new_youtube_id = request.form.get('new_youtube_id')

        # If the user sends a link and not an id, quietly delete the parts that don't matter.
        new_youtube_id = new_youtube_id.replace(
            'https://www.youtube.com/watch?v=', '')
        new_youtube_id = new_youtube_id.replace('https://youtu.be/', '')

        # Read the video list.
        video_list = db_tools.get_videos()

        # TODO: Make this into a list comprehension.
        # Basically, search for the id you want to replace, replace it, write your changes to a new list.
        video_list2 = []
        for video in video_list:
            if old_youtube_id in video:
                i = i.replace(old_youtube_id, new_youtube_id)
            video_list2.append(i)

        # Point the old list to your new one.
        video_list = video_list2

        # Overwrite and reload. You know the drill.
        db_tools.overwrite_videos(video_list)
        return redirect('../videos')

    # The move up and move down buttons send data here.
    @app.route('/videos/move', methods=["POST"])
    @login_required(must=have_access_to_admin)
    def move():
        # This is the EXACT element in the video list. If its not, it'll cause a ValueError.
        video_list_element = request.form.get('element')+'\n'

        # The direction to move the video, 'up' or 'down'
        direction = request.form.get('direction')

        # Again, just reading the video list.
        video_list = db_tools.get_videos()

        # Find the index for the desired element.
        videoindex = video_list.index(video_list_element)

        # Remove the element at that position. Without this line,
        # the video will appear twice, both in the old position, and the new one.
        video_list.pop(videoindex)

        # Now, shift the index by one.
        if direction == 'up':
            # I know subtracting seems counter-intuitive, but remember, index 0 is the top of the list.
            videoindex -= 1
        else:
            # The bigger index, the lower on the list.
            videoindex += 1

        # Insert the element, exactly as it was, in its new position, exactly one higher or one lower.
        video_list.insert(videoindex, video_list_element)

        # Overwrite and refresh.
        db_tools.overwrite_videos(video_list)
        return redirect('../videos')
###########
#Messenger#
###########


def messenger():
    # Main page
    @app.route('/messenger')
    def messenger_main_page():
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

    # When the user sends a message, it goes here.
    @app.route('/messenger/result', methods=['POST', 'GET'])
    def new_message():
        if request.method == 'POST':
            message = request.form.get('Data')
            db_tools.add_message(message)
        return redirect('/messenger')
    @app.route('/message/stream')
    def message_stream():
        def eventStream():
            previous_messages=db_tools.read_messages()
            while True:
                time.sleep(15)
                messages = db_tools.read_messages()
                if previous_messages != messages:
                    previous_messages=messages
                    formatted_messages = [''.join(i) for i in messages]
                    pp.pprint(formatted_messages)
                    yield "data: {}\n\n".format(formatted_messages[-1])
        return Response(eventStream(), mimetype="text/event-stream")
    # Clear messages
    @app.route('/messenger/clear', methods=['POST', 'GET'])
    def clear_all_messages():
        db_tools.clear_messages()
        return redirect('/messenger')

########
#Prayer#
########


def prayer():
    # The main page
    @app.route('/prayer')
    def prayer_page():
        return render_template('prayer.html')

    @app.route('/FlaskApp/prayer')
    def old_prayer_page():
        return redirect('/prayer')

    # Email submissions
    @app.route('/prayer/newemail', methods=['POST', 'GET'])
    def new_email():
        if request.method == 'POST':
            email = request.form.get('email')
            parish = request.form.get('parish')
            parish = parish.upper()

            # This is a dictionary that converts the code the user typed in into a parish.
            # If adding a new group:
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
                email, "Thank you for joining JMJprayerrequests", message, PROJECT_EMAIL, PROJECT_PASSWORD)
            # Displays a page with further instruction
            return render_template('email_adding.html')

    # The second step of verification
    # This uses get instead of post in hopes of greater
    # compatibility with email clients.
    @app.route('/prayer/newemailconfirmed')
    def new_email_confirmed():
        code = request.args.get('code')
        address = request.args.get('email')
        parish = request.args.get('parish')
        if len(code)==0:
            return("""No verification code was recieved. Please try again.
            Theres two reasons why this could've happened: <ol>
            <li>I messed up something with the code.</li>
            <li>You messed with something you weren't supposed to.</li></ol>
            </li>If you happen to be me, it's probably both. If you aren't me, feel free to email me if you think it's broken, or to try again if you think you broke it.
            If problem persists, send me an email describing the problem. <br / >
            <br/><img src='https://imgs.xkcd.com/comics/unreachable_state.png'/>""")
        try:
            verification_result = db_tools.check_verification_code(code)
        except TypeError:
            return """<html><p>Verification Failed. Your email client may not be supported. Try a different client, e.g. Outlook, your email provider's website, the mail app on your phone, etc.</p>
                      <br/><img src='https://imgs.xkcd.com/comics/unreachable_state.png'/></html>"""

        if verification_result:  # If verification succeeds:
            # Adds email to applicable groups
            db_tools.add_to_mailing_list(address, parish)
            db_tools.add_to_mailing_list(address, "Public")
            if "RE" in parish:
                new_parish = parish.replace('RE', 'Parish')
                db_tools.add_to_exiymailing_list(address, new_parish)

            # Returns success page.
            return render_template('email_added.html')
        else:
            # Returns failure message.
            return """Email verification failed. Verification code is invalid or expired. Please try signing up again.
            If the problem persists, click "Contact" and send me an email describing your issue. Sorry!"""

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
        # Uncommenting this is a really, really bad idea.
        # emails=[personalemail]

        for email in emails:
            send_email(email, subject_template, message_template,
                       PROJECT_EMAIL, PROJECT_PASSWORD)
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
    def new_todo():
        name = request.form.get('taskname')
        name = name.replace(',', 'COMMA')
        db_tools.add_todo(name)
        send_email('todo+19z1n4ovd3rf@mail.ticktick.com', name, 'Submitted from jforseth.tech',
                   PERSONAL_EMAIL, PERSONAL_PASSWORD)

        return redirect('/todo')

    # Deletion route
    @app.route('/todo/delete', methods=['POST', 'GET'])
    @login_required(must=have_access_to_todo)
    def todo_deleted():
        try:
            task_id = int(request.form.get('taskid'))
        except ValueError:
            return 'Please enter a number...'
        db_tools.delete_todo(task_id)
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


def farm_year_video():
    @app.route('/FarmYearVideo')
    def farm_year_video_page():
        return render_template('FarmYearVideo.html')

    @app.route('/farmyearvideo')
    def farm_year_video_page1():
        return render_template('FarmYearVideo.html')

    @app.route('/farm_year_video')
    def farm_year_video_page2():
        return render_template('FarmYearVideo.html')

    @app.route('/Farm_Year_Video')
    def farm_year_video_page3():
        return render_template('FarmYearVideo.html')

    @app.route('/FARMYEARVIDEO')
    def farm_year_video_page4():
        return render_template('FarmYearVideo.html')

    @app.route('/FARM_YEAR_VIDEO')
    def farm_year_video_page5():
        return render_template('FarmYearVideo.html')

###########
#Quickdraw#
###########


def quickdraw_game():
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
    def big_screen():
        return render_template('bigscreen.html')

    @app.route('/quickdraw/bigscreen/begin')
    def big_screen_begin():
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


def bull_judging():
    @app.route('/bulljudging')
    def bull_judging_homepage():
        return render_template("bulljudginghome.html")

    @app.route('/bulljudging1')
    def bull_judging1():
        return render_template("bulljudging1.html")

    @app.route('/bulljudging2')
    def bull_judging2():
        return render_template("bulljudging2.html")

    @app.route('/bulljudging3')
    def bull_judging3():
        return render_template("bulljudging3.html")

    @app.route('/bulljudging4')
    def bull_judging4():
        return render_template("bulljudging4.html")

    @app.route('/bulljudgingdone')
    def bull_judging_done():
        return render_template("bulljudgingdone.html")
#######
#Admin#
#######


def admin():
    @app.route('/DBbrowser')
    @login_required(must=have_access_to_admin)
    def database_browser():
        messages = db_tools.get_all_from_table("messages")
        accounts = db_tools.get_all_from_table("accounts")
        users = db_tools.get_all_from_table("users")
        return "Messages: <br />{}<br />Accounts:<br />{}<br />Users:<br />{}<br />".format(messages, accounts, users)

##############
#File Sharing#
##############


def file_sharing():
    # This is a magic function from the flask documentation. I have no idea what it does or how it works.
    def allowed_file(file_name):
        return '.' in file_name and \
            file_name.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    # Again. I'd like to change this to file_name, but I think it'd break something.
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

            # TODO: Figure out how on earth url_for works
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                return redirect(url_for('uploaded_file', filename=filename))

        else:
            file_list = os.listdir(app.config['UPLOAD_FOLDER'])
            return render_template('file_sharing.html', files=file_list)

    @app.route('/filesharing/<filename>')
    def uploaded_file(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'],
                                   filename)

    @app.route('/filesharing/filelist')
    def file_list():
        files = os.listdir(app.config['UPLOAD_FOLDER'])
        return ''.join(files)
######
#Misc#
######
def barrel_racing():
    #@app.route('/barrelracing')
    #def barrel_racing():
    #    return redirect("https://sites.google.com/view/mtbrda/home")
    @app.route('/barrelracing/app_lab')
    def barrel_racing_app_lab():
        return render_template('AP Create Task/index.html')
    @app.route('/barrelracing/counter')
    def barrel_racing_counter():
        with open("text/barrel_racing_current_number.txt",'r') as file:
            current_number=file.readline()
        try:
            current_number=int(current_number)
        except ValueError:
            return "Please enter a number"
        return render_template("barrel_racing_counter.html",current_number=current_number,current_number_plus=current_number+1,current_number_minus=current_number-1)
    @app.route('/barrelracing/counter/currentnumber')
    def barrel_racing_counter_current_number():
        with open("text/barrel_racing_current_number.txt",'r') as file:
            current_number=file.readline()
        return current_number
    @app.route('/barrelracing/current_number_update',methods=['POST'])
    def barrel_racing_current_number_update():
        current_number=request.form.get("current_number")
        with open("text/barrel_racing_current_number.txt",'w') as file:
            file.write(current_number)
        return redirect("/barrelracing/counter")
    @app.route('/barrelracing/stream')
    def barrelracing_stream():
        def eventStream():
            old_current_number=''
            with open("text/barrel_racing_current_number.txt",'r') as file:
                    old_current_number=file.readline()
            while True:
                time.sleep(15)
                with open("text/barrel_racing_current_number.txt",'r') as file:
                    current_number=file.readline()
                if old_current_number != current_number:
                    old_current_number=current_number
                    yield "data: {}\n\n".format(current_number)
        return Response(eventStream(), mimetype="text/event-stream")
def scattergories():
    @app.route('/scattergories')
    def scattergories_page():
        with open(r"text/currentcatergorylist.txt") as file:
            category_list = file.readlines()

        category_list = [i.replace('\n', '') for i in category_list]

        with open(r"text/scattergoriescurrentletter.txt") as file:
            current_letter = file.read()
        return render_template("Scattergories.html", list=category_list, current_letter=current_letter)

    @app.route('/scattergories/newlist')
    def scattergories_new_list():
        with open(r"text/allcatergorylist.txt") as file:
            CATERGORY_LIST = file.readlines()
        CATERGORY_LIST = [i.replace('\n', '').title() for i in CATERGORY_LIST]
        new_list = []
        for i in range(12):
            new_list.append(random.choice(CATERGORY_LIST))
        with open(
                r"text/currentcatergorylist.txt", "w") as file:

            file.writelines(["%s\n" % item for item in new_list])
        return "Done"

    @app.route('/scattergories/roll')
    def scattergories_roll():
        LETTERS = string.ascii_uppercase
        letter = random.choice(LETTERS)
        file = open(r"text/scattergoriescurrentletter.txt", "w")
        file.write(letter)
        file.close()
        return "Done!"
        # Running all of the above
################
#Error Handlers#
################


def error_handlers():
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    @app.errorhandler(403)
    def forbidden(e):
        return render_template('403.html'), 403

    @app.errorhandler(500)
    def server_error(e):
        return render_template('500.html'), 500


# Most functions of jforseth.tech can be disabled by commenting out
# the appropriate line. Not this doesn't update the frontend and may cause
# 404s
welcome()
videos()
messenger()
prayer()
todo()
farm_year_video()
admin()
error_handlers()
# bull_judging()
file_sharing()
# scattergories()
# quickdraw_game()
barrel_racing()

# Runs the testing server.
if __name__ == "__main__":
    app.debug = True
    app.run()
