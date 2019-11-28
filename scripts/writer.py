from flask import *
import os 
import io
import time
import os.path
from werkzeug.utils import secure_filename
from account_management import have_access_to_writer
from flask_simplelogin import login_required
writer = Blueprint('writer', __name__)

WRITER_PATH="text/writerdocs"

@writer.route('/writer')
@login_required(must=have_access_to_writer)
def writer_home():
    files = os.listdir(WRITER_PATH)
    new_files=[]
    for i in files:
        i=i.replace('.html',"")
        new_files.append(i)
    return render_template("writer/writer.html",docs=new_files)

@writer.route('/writer/thumb/<name>')
def writer_thumb(name):
    try:
        return send_file('static/writer_thumbs/{}.html_thumb.png'.format(name))
    except IOError:
        print("Generating new thumb")
        imgkit.from_file(WRITER_PATH+"/"+name+".html", 'static/writer_thumbs/{}_thumb.png'.format(name),config=config,options=options)
        time.sleep(1)
        return send_file('static/writer_thumbs/{}.html_thumb.png'.format(name))
@writer.route('/writer/<name>')
@login_required(must=have_access_to_writer)
def writer_page(name):
    #with io.open("The Healer.html",encoding="utf-8") as file:
    #    document=file.read()
    #document=Markup(document)    
    return render_template("writer/Summernote.html",name=name)
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
