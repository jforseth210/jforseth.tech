from flask import *
import time
barrel_racing=Blueprint("barrel_racing", __name__)
#@barrel_racing.route('/barrelracing')
#def barrel_racing():
#    return redirect("https://sites.google.com/view/mtbrda/home")
@barrel_racing.route('/barrelracing/app_lab')
def barrel_racing_app_lab():
    return render_template('AP Create Task/index.html')
@barrel_racing.route('/barrelracing/counter')
def barrel_racing_counter():
    with open("text/barrel_racing_current_number.txt",'r') as file:
        current_number=file.readline()
    try:
        current_number=int(current_number)
    except ValueError:
        return "Please enter a number"
    return render_template("barrel_racing_counter.html",current_number=current_number,current_number_plus=current_number+1,current_number_minus=current_number-1)
@barrel_racing.route('/barrelracing/counter/currentnumber')
def barrel_racing_counter_current_number():
    with open("text/barrel_racing_current_number.txt",'r') as file:
        current_number=file.readline()
    return current_number
@barrel_racing.route('/barrelracing/current_number_update',methods=['POST'])
def barrel_racing_current_number_update():
    current_number=request.form.get("current_number")
    with open("text/barrel_racing_current_number.txt",'w') as file:
        file.write(current_number)
    return redirect("/barrelracing/counter")
@barrel_racing.route('/barrelracing/stream')
def barrelracing_stream():
    def eventStream():
        old_current_number=''
        with open("text/barrel_racing_current_number.txt",'r') as file:
                old_current_number=file.readline()
        while True:
            time.sleep(10)
            with open("text/barrel_racing_current_number.txt",'r') as file:
                current_number=file.readline()
            if old_current_number != current_number:
                old_current_number=current_number
                yield "data: {}\n\n".format(current_number)
    return Response(eventStream(), mimetype="text/event-stream")
