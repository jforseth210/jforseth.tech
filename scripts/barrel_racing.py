import time

from flask import *

barrel_racing = Blueprint("barrel_racing", __name__)


@barrel_racing.route("/barrelracing/app_lab")
def barrel_racing_app_lab():
    return "AP Create Task/index.html"


@barrel_racing.route("/barrelracing/counter")
def barrel_racing_counter():
    with open("/var/www/jforseth.tech/text/barrel_racing_current_number.txt", "r") as file:
        current_number = file.readline()
            
    try:
        current_number = int(current_number)
    except ValueError:
        flash("Current number is not a number! Please type in a number.",
              category="alert")
        return render_template("barrel_racing/barrel_racing_counter.html", current_number="ERROR")
    with open("/var/www/jforseth.tech/text/barrel_racing_best_time.txt", 'r') as file:
        current_best = file.readline()
    with open("/var/www/jforseth.tech/text/barrel_racing_horse_rate.txt", 'r') as file:
        current_rate = file.readline()
    return render_template("barrel_racing/barrel_racing_counter.html", current_number=current_number,best_time=current_best,current_rate=current_rate)


@barrel_racing.route('/barrelracing/counter/currentnumber')
def barrel_racing_counter_current_number():
    with open("/var/www/jforseth.tech/text/barrel_racing_current_number.txt", "r") as file:
        current_number = file.readline()
    return current_number


@barrel_racing.route("/barrelracing/current_number_update", methods=["POST"])
def barrel_racing_current_number_update():
    current_number = escape(request.form.get("current_number"))
    try:
        int(current_number)
        with open("/var/www/jforseth.tech/text/barrel_racing_current_number.txt", "w") as file:
            file.write(current_number)
    except:
        flash("Please enter a number", category="warning")
    return redirect("/barrelracing/counter")

@barrel_racing.route('/barrelracing/best_time_update', methods=['POST'])
def barrel_racing_best_time_update():
    best_time = escape(request.form.get("best_time"))
    with open("/var/www/jforseth.tech/text/barrel_racing_best_time.txt", 'w') as file:
        file.write(best_time)
    return redirect("/barrelracing/counter")

@barrel_racing.route('/barrelracing/current_rate_update', methods=['POST'])
def barrel_racing_current_rate_update():
    current_rate = escape(request.form.get("current_rate"))
    with open("/var/www/jforseth.tech/text/barrel_racing_horse_rate.txt", 'w') as file:
        file.write(current_rate)
    return redirect("/barrelracing/counter")

@barrel_racing.route('/barrelracing/counter/stream')
def barrelracing_counter_stream():
    def eventStream():
        with open("/var/www/jforseth.tech/text/barrel_racing_current_number.txt", "r") as file:
            old_current_number = file.readline()
        while True:
            time.sleep(1)
            with open("/var/www/jforseth.tech/text/barrel_racing_current_number.txt", 'r') as file:

                current_number = file.readline()
            if old_current_number != current_number:
                old_current_number = current_number
                yield "data: {}\n\n".format(current_number)

    return Response(eventStream(), mimetype="/var/www/jforseth.tech/text/event-stream")

@barrel_racing.route('/barrelracing/best_time/stream')
def barrelracing_best_time_stream():
    def eventStream():
        with open("/var/www/jforseth.tech/text/barrel_racing_best_time.txt", 'r') as file:
            old_best = file.readline()
        while True:
            time.sleep(1)
            with open("/var/www/jforseth.tech/text/barrel_racing_best_time.txt", 'r') as file:
                current_best = file.readline()
            if old_best != current_best:
                old_best = current_best
                yield "data: {}\n\n".format(current_best)
    return Response(eventStream(), mimetype="/var/www/jforseth.tech/text/event-stream")

@barrel_racing.route('/barrelracing/horse_rate/stream')
def barrelracing_horse_rate_stream():
    def eventStream():
        with open("/var/www/jforseth.tech/text/barrel_racing_horse_rate.txt", 'r') as file:
            old_rate = file.readline()
        while True:
            time.sleep(1)
            with open("/var/www/jforseth.tech/text/barrel_racing_horse_rate.txt", 'r') as file:
                current_rate = file.readline()
            if old_rate != current_rate:
                old_rate = current_rate
                yield "data: {}\n\n".format(current_rate)
    return Response(eventStream(), mimetype="/var/www/jforseth.tech/text/event-stream")