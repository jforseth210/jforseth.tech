from flask import *

LQA = Blueprint('LQA', __name__)
CHOICES = {
    '1':[(2,"It'll be fine. Go buy your animal."),(3,"Fix the panel and clean out the pen.")],
    '2':[(3,"Continue")],
    '3':[(4,"Remain calm"),(11,"Kick your animal")],
    '4':[(5,"Call the vet."),(6,"Check the waterer")],
    '5':[(6,"Continue")],
    '6':[(7,"Mix the finisher with the grower slowly"),(12,"Wait until you run out of grower, then switch.")],
    '7':[(8,"Continue")],
    '8':[(9,"Throw it out."),(10,"Keep it for 3 years.")],
    '9':[(10,"Continue")],
    '10':[(13,"Play tag with your friends in the barns."),(14,"Clean your animal's pen, help other 4-Hers")],
    '11':[(4,"Continue")],
    '12':[(7,"I still have my spare!"),(7,"That was my spare. I guess I'll help my friends.")],
    '13':[(15,"Continue")],
    '14':[(1,"Play Again")],
    '15':[(1,"Try Again")]
}
@LQA.route("/lqa")
def lqa():
    return load_lqa_temp('1')

@LQA.route("/lqa/<station>")
def lqa_station(station):
    return load_lqa_temp(station)

def load_lqa_temp(current_station):
    with open("text/lqa/Station{}.html".format(current_station)) as file:
        station_text=Markup(file.read())
    print(CHOICES[current_station])
    return render_template('LQA/lqa.html',station_text=station_text, choices=CHOICES[current_station])