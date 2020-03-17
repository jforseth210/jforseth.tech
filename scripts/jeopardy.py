from flask import *
import time
import os
import random
import pprint as pp
jeopardy = Blueprint('jeopardy', __name__)

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
    flash(Markup("Warning!<br/><img style='text-align:center'src=https://imgs.xkcd.com/comics/pandora.png />"))
    return render_template("jeopardy/jeopardy.html",clues=clues)  
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
    return render_template('jeopardy/jeopardy_buzzer.html')
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
    final=listsongs("Final")[0]
    print(final)
    return final