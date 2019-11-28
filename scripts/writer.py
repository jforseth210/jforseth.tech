from flask import *
import os 
import io
from werkzeug.utils import secure_filename
from account_management import have_access_to_writer
from flask_simplelogin import login_required
writer = Blueprint('writer', __name__)
@writer.route('/writer')
@login_required(must=have_access_to_writer)
def writer_home():
    WRITER_PATH="text/writerdocs"
    files = os.listdir(WRITER_PATH)
    new_files=[]
    for i in files:
        i=i.replace('.html',"")
        i="<a href='/writer/{}'>{}</a><br/>".format(i,i)
        new_files.append(i)
    return "".join(new_files)
@writer.route('/writer/<name>')
@login_required(must=have_access_to_writer)
def writer_page(name):
    #with io.open("The Healer.html",encoding="utf-8") as file:
    #    document=file.read()
    #document=Markup(document)    
    return render_template("Summernote.html",name=name)
@writer.route('/writer/save/<name>', methods=["POST"])
@login_required(must=have_access_to_writer)
def save(name):
    name=secure_filename(name)
    data=request.form.get("text")
    with io.open("text/writerdocs/{}.html".format(name), "w", encoding="utf-8") as file:
        document=file.write(data)
    return ""
@writer.route('/writer/document/<name>')
@login_required(must=have_access_to_writer)
def document(name):
    name=secure_filename(name)
    try:
        with io.open("text/writerdocs/{}.html".format(name), "r", encoding="utf-8") as file:
            document=file.read()
    #except FileNotFoundError:
    #    io.open("text/writerdocs/{}.html".format(name))
    #    document=""
    except IOError: #Python2
        io.open("text/writerdocs/{}.html".format(name),"w")
        document=""
    return Markup(document)
