import random
import string

from flask import *

scattergories = Blueprint("scattergories", __name__)


@scattergories.route("/scattergories")
def scattergories_page():
    with open(r"/var/www/jforseth.tech/text/currentcatergorylist.txt") as file:
        category_list = file.readlines()

    category_list = [i.replace("\n", "") for i in category_list]

    with open(r"/var/www/jforseth.tech/text/scattergoriescurrentletter.txt") as file:
        current_letter = file.read()
    return render_template(
        "scattergories/scattergories.html",
        list=category_list,
        current_letter=current_letter,
    )


@scattergories.route("/scattergories/newlist")
def scattergories_new_list():
    with open(r"/var/www/jforseth.tech/text/allcatergorylist.txt") as file:
        CATERGORY_LIST = file.readlines()
    CATERGORY_LIST = [i.replace("\n", "").title() for i in CATERGORY_LIST]
    new_list = [random.choice(CATERGORY_LIST) for i in range(12)]
    with open(r"/var/www/jforseth.tech/text/currentcatergorylist.txt", "w") as file:

        file.writelines(["%s\n" % item for item in new_list])
    return "Done"


@scattergories.route("/scattergories/roll")
def scattergories_roll():
    LETTERS = string.ascii_uppercase
    letter = random.choice(LETTERS)
    with open(r"/var/www/jforseth.tech/text/scattergoriescurrentletter.txt", "w") as file:
        file.write(letter)
    return "Done"
    # Running all of the above
