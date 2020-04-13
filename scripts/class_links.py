from flask import *
import sqlite3
from account_management import have_access_to_class_links
from flask_simplelogin import login_required

class_links = Blueprint('class_links', __name__)
class card():
    def __init__(self,category,name,items,profile_image):
        self.category=category
        self.name=name
        self.items=items
        self.profile_image=profile_image
class course():
    def __init__(self,period,name,link):
        self.period=period
        self.name=name
        self.link=link
def get_cards():
    conn=sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    
    cur.execute("""SELECT * FROM class_links""")
    rows=cur.fetchall()
    cards=[]
    for row in rows:
        courses=row['items'].split("\n")
        items=[]
        for i in courses:
            i=i.split(',')
            items.append(course(i[0],i[1],i[2]))
        cards.append(card(row['category'],row['name'],items,row['profile_image']))
    return cards
def get_unique_categories():
    conn=sqlite3.connect('database.db')
    cur = conn.cursor()
    
    cur.execute("""SELECT DISTINCT category FROM class_links""")
    categories=cur.fetchall()
    categories=[category[0] for category in categories]
    return categories
@class_links.route("/classes")
@login_required(must=have_access_to_class_links)
def class_links_home():
    cards=get_cards()
    categories=get_unique_categories()
    print(cards[0].profile_image)
    return render_template("class_links/gallery.html",categories=categories,cards=cards)