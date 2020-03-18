from flask import *
import time
import os
import random
import pprint as pp
jeopardy = Blueprint('jeopardy', __name__)

names=sorted(["Mom","Dad","Justin","Nolan"])

PATH=r"C:\\Users\\Forseth\\Music\\Music Jeopardy\\"
def listsongs(person):
    files=[]
    print(PATH+person)
    for r,_,f in os.walk(PATH+person):
        for file in f:
            files.append(os.path.join(r,file))
    return random.sample(files,6)
@jeopardy.route('/jeopardy')
def welcome_page():
    clues = {
        "Mom":listsongs("Mom"),
        "Dad":listsongs("Dad"),
        "Justin":listsongs("Justin"),
        "Nolan":listsongs("Nolan")
    }
    with open("text/jeopardy_final.txt", "w") as file:
        file.write("False")
    with open("text/final_jeopardy_submission.txt", "w") as file:
        file.write("")
    return render_template("jeopardy/jeopardy.html",clues=clues,names=names)  
@jeopardy.route("/jeopardy/song")
def song():
    song=request.args.get('song')
    return send_file(song,mimetype="audio/m4a",as_attachment=True,attachment_filename=song)

@jeopardy.route("/jeopardy/buzzerstream")
def buzzerstream():
    def eventStream():
        with open("text/jeopardy_buzzer.txt", 'r') as file:
            old_buzzer = file.read()
        while True:
            time.sleep(0.5)
            with open("text/jeopardy_buzzer.txt", 'r') as file:
                buzzer = file.read()
            if buzzer != "False,RESET":
                buzzer=buzzer.split(',')[1]
                yield "data: {}\n\n".format(buzzer)
            else:
                pass #yield "data: {}\n\n".format("I'm alive!")
    return Response(eventStream(), mimetype="text/event-stream")
@jeopardy.route('/jeopardy/buzzer')
def buzzer():
    return render_template('jeopardy/jeopardy_buzzer.html',names=names)
@jeopardy.route('/jeopardy/buzzedin')
def buzzedin():
    name=request.args.get("name")
    with open('text/jeopardy_buzzer.txt') as file:
        current_buzzer=file.read()
    if name == "False,RESET":
        with open('text/jeopardy_buzzer.txt','w') as file:
            file.write(name)
    elif current_buzzer.split(',')[0] =="False":
        with open('text/jeopardy_buzzer.txt','w') as file:
            file.write("True,"+name)
    return redirect("jeopardy/buzzer")

@jeopardy.route("/jeopardy/final")
def final():
    with open("text/final_jeopardy_submission.txt", "w") as file:
        file.write("")
    final=listsongs("Final")[0]
    print(final)
    with open("text/jeopardy_final.txt", "w") as file:
        file.write("True")
    return final

@jeopardy.route("/jeopardy/finalstream")
def finalstream():
    def eventStream():
        while True:
            time.sleep(0.5)
            with open("text/jeopardy_final.txt", 'r') as file:
                final = file.read()
            if final == "True":
                yield "data: {}\n\n".format(final)
    return Response(eventStream(), mimetype="text/event-stream")

@jeopardy.route("/jeopardy/final_submissions")
def final_submissions():
    name=request.args.get('name')
    wager=request.args.get('wager')
    answer=request.args.get('answer')
    with open("text/final_jeopardy_submission.txt","a") as file:
        file.write("\n{},{},{}".format(name,wager,answer))
    return "Done!"

@jeopardy.route("/jeopardy/finalresponses")
def final_responses():
    with open("text/final_jeopardy_submission.txt") as file:
        responses=file.read()
    return str(responses)