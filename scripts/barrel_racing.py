import time

from flask import *
barrel_racing = Blueprint("barrel_racing", __name__)

# TODO: Talk to Rylan about depreciating this?


@barrel_racing.route('/barrelracing/app_lab')
def barrel_racing_app_lab():
    return ('AP Create Task/index.html')


@barrel_racing.route('/barrelracing/counter')
def barrel_racing_counter():
    with open("text/barrel_racing_current_number.txt", 'r') as file:
        current_number = file.readline()
    try:
        current_number = int(current_number)
    except ValueError:
        flash("Current number is not a number! Please type in a number.",
              category="alert")
        return render_template("barrel_racing/barrel_racing_counter.html", current_number="ERROR")
    return render_template("barrel_racing/barrel_racing_counter.html", current_number=current_number)


@barrel_racing.route('/barrelracing/counter/currentnumber')
def barrel_racing_counter_current_number():
    with open("text/barrel_racing_current_number.txt", 'r') as file:
        current_number = file.readline()
    return current_number


@barrel_racing.route('/barrelracing/current_number_update', methods=['POST'])
def barrel_racing_current_number_update():
    current_number = escape(request.form.get("current_number"))
    try:
        int(current_number)
        with open("text/barrel_racing_current_number.txt", 'w') as file:
            file.write(current_number)
    except:
        flash("Please enter a number", category="warning")
    return redirect("/barrelracing/counter")


@barrel_racing.route('/barrelracing/stream')
def barrelracing_stream():
    def eventStream():
        with open("text/barrel_racing_current_number.txt", 'r') as file:
            old_current_number = file.readline()
        while True:
            time.sleep(10)
            with open("text/barrel_racing_current_number.txt", 'r') as file:
                current_number = file.readline()
            if old_current_number != current_number:
                old_current_number = current_number
                yield "data: {}\n\n".format(current_number)
    return Response(eventStream(), mimetype="text/event-stream")
