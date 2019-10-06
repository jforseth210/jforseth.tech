from flask import *
import random
import string

scattergories = Blueprint("scattergories", __name__)


@scattergories.route('/scattergories')
def scattergories_page():
    with open(r"text/currentcatergorylist.txt") as file:
        category_list = file.readlines()

    category_list = [i.replace('\n', '') for i in category_list]

    with open(r"text/scattergoriescurrentletter.txt") as file:
        current_letter = file.read()
    return render_template("Scattergories.html", list=category_list, current_letter=current_letter)


@scattergories.route('/scattergories/newlist')
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


@scattergories.route('/scattergories/roll')
def scattergories_roll():
    LETTERS = string.ascii_uppercase
    letter = random.choice(LETTERS)
    file = open(r"text/scattergoriescurrentletter.txt", "w")
    file.write(letter)
    file.close()
    return "Done!"
    # Running all of the above
