from flask import *
from account_management import have_access_to_lqa
from flask_simplelogin import login_required

LQA = Blueprint('LQA', __name__)
CHOICES = {
    '1':[(2,"A"),(3,"B")],
    '2':[(3,"Continue")],
    '3':[(4,"A"),(11,"B")],
    '4':[(5,"A"),(6,"B")],
    '5':[(6,"Continue")],
    '6':[(7,"A"),(12,"B")],
    '7':[(8,"Continue")],
    '8':[(9,"A"),(10,"B")],
    '9':[(10,"Continue")],
    '10':[(13,"A"),(14,"B")],
    '11':[(4,"Continue")],
    '12':[(7,"A"),(7,"B")],
    '13':[(15,"Continue")],
    '14':[(1,"Play Again")],
    '15':[(1,"Try Again")]
}
@LQA.route("/lqa")
@login_required(must=have_access_to_lqa)
def lqa():
    return load_lqa_temp('1')

@LQA.route("/lqa/<station>")
@login_required(must=have_access_to_lqa)
def lqa_station(station):
    return load_lqa_temp(station)

def load_lqa_temp(current_station):
    with open("text/lqa/Station{}.html".format(current_station)) as file:
        station_text=Markup(file.read())
    print(CHOICES[current_station])
    return render_template('LQA/lqa.html',station_text=station_text, choices=CHOICES[current_station])