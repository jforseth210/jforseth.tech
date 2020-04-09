from flask import *
from account_management import have_access_to_class_links
from flask_simplelogin import login_required

class_links = Blueprint('class_links', __name__)
class card():
    def __init__(self,category,name,items):
        self.category=category
        self.name=name
        self.items=items
class course():
    def __init__(self,period,name,link):
        self.period=period
        self.name=name
        self.link=link
park=card(
    "Classes",
    "John Park",
    [course('1','Ag Mechanics','https://zoom.com'),course("2b","Small Engines","https://zoom.com")]
)
@class_links.route("/classes")
@login_required(must=have_access_to_class_links)
def class_links_home():
    return render_template("class_links/gallery.html",categories=["Classes","Clubs","Other"],cards=[park])