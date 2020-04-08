from flask import *
from account_management import have_access_to_class_links
from flask_simplelogin import login_required

class_links = Blueprint('class_links', __name__)
@class_links.route("/classes")
@login_required(must=have_access_to_class_links)
def class_links_home():
    return "Hello!"