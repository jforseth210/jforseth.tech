from flask import *

from account_management import have_access_to_lqa
from flask_simplelogin import login_required

LQA = Blueprint('LQA', __name__)
CHOICES = {
    '1':[(2,"Option A"),(3,"Option B")],
    '2':[(3,"Continue")],
    '3':[(4,"Option A"),(11,"Option B")],
    '4':[(5,"Option A"),(6,"Option B")],
    '5':[(6,"Continue")],
    '6':[(7,"Option A"),(12,"Option B")],
    '7':[(8,"Continue")],
    '8':[(9,"Option A"),(10,"Option B")],
    '9':[(10,"Continue")],
    '10':[(13,"Option A"),(14,"Option B")],
    '11':[(4,"Continue")],
    '12':[(7,"Option A"),(15,"Option B")],
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