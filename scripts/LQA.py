from flask import *
from account_management import have_access_to_lqa
from flask_simplelogin import login_required

LQA = Blueprint('LQA', __name__)
CHOICES = {
    '1':[(2,"You are running late and don’t have time to fix the panel and clean the pen.  You’ll do it later."),(3,"You call the breeder, apologize, and tell them you will be late.  You fix the panel and clean the pen and then go pick up your animal.")],
    '2':[(3,"Continue")],
    '3':[(4,"You remain calm and keep working patiently with your animal.  It will take time to train your animal."),(11,"You are so frustrated that you yell at your animal and kick at it as hard as you can.")],
    '4':[(5,"You think your animal might be sick.  You call the vet and leave the water, for now."),(6,"You decide to clean the water and see if your animal starts drinking again.")],
    '5':[(6,"Continue")],
    '6':[(7,"You mix finisher feed in with the grower feed slowly to get your animal used to the change in feed."),(12,"You feed your animal the rest of the grower feed, and then switch to the finisher feed.")],
    '7':[(8,"Continue")],
    '8':[(9,"You don’t own the animal anymore, so you decide to throw it away."),(10,"You decide to keep your treatment record in a safe place for three years.")],
    '9':[(10,"Continue")],
    '10':[(13,"You decide to get a group of friends together and play tag, running and yelling in the barns by the animals."),(14,"You clean your animal’s pen and help other 4-H members get their animals ready.")],
    '11':[(4,"Continue")],
    '12':[(7,"If you still have a buddy animal, click here."),(7,"If you no longer have a buddy animal, this is the end of your project year. Click here.")],
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