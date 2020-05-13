from flask import *
import os
import io
import time
import platform
import os.path
from werkzeug.utils import secure_filename
from SensitiveData import ANDROID_ID
#from account_management import have_access_to_writer
from flask_simplelogin import login_required, get_username
from refresh_writer_thumbs import refresh_thumbs
writer = Blueprint('writer', __name__)

#TODO: Add multiaccount support to writer app. 
#TODO: Massive app refactor

@writer.route('/writer')
@login_required()
def writer_home():
    if platform.node() == "backup-server-vm":
        flash("The main jforseth.tech server is currently experiencing issues. Your changes may not be saved when the main server comes back online.")
    username = get_username()
    path = "userdata/{}/writer/documents/".format(username)
    print(path)
    if not os.path.isdir(path):
        os.makedirs(path)
        os.makedirs("userdata/{}/writer/thumbnails/".format(username))
    files = os.listdir(path)
    files = [i for i in files if i!='oopsie']
    new_files = []
    for i in files:
        if i != 'oopsie':
            i = i.replace('.html', "")
            i = i.title()
            new_files.append(i)
    return render_template("writer/writer.html", docs=new_files)


@writer.route('/writer/thumb/<name>')
def writer_thumb(name):
    try:
        return send_file('userdata/{}/writer/thumbnails/{}.html_thumb.png'.format(get_username(),name.lower()))
    except:
        refresh_thumbs(get_username())
        return send_file('userdata/{}/writer/thumbnails/{}.html_thumb.png'.format(get_username(),name.lower()))


@writer.route('/writer/<name>')
@login_required()
def writer_page(name):
    # with io.open("The Healer.html",encoding="utf-8") as file:
    #    document=file.read()
    # document=Markup(document)
    return render_template("writer/Summernote.html", name=name)


@writer.route('/writer/save/<name>', methods=["POST"])
@login_required()
def web_save(name):
    data = request.form.get("editordata")
    return save(name, data)


"""@writer.route("/writer/api/save/<name>", methods=["POST"])
def api_save(name):
    request_id = request.form.get("id")
    data = request.form.get("editordata")
    if request_id == ANDROID_ID:
        save(name, data)
        return ""
    else:
        print(ANDROID_ID, request_id)
        return "Invalid id."
"""
@writer.route('/writer/document/<name>')
@login_required()
def document_noapi(name):
    document = get_document(name)
    return document


"""@writer.route("/writer/api/document/<name>")
def document_api(name):
    request_id = request.args.get("id")
    if request_id == ANDROID_ID:
        requested_document = get_document(name)
        return requested_document
    else:
        print(ANDROID_ID, request_id)
        return "Invalid id."
"""
def save(filename, data):
    filename = secure_filename(filename)
    filename = filename.lower()
    username = get_username()
    path = "userdata/{}/writer/documents/".format(username)
    if not os.path.isdir(path):
        os.makedirs(path)

    print(data)
    print(path+"{}.html".format(filename))
    with io.open(path+"{}.html".format(filename), "w", encoding="utf-8") as file:
        file.write(data)
        print("Wrote {} to {}".format(data, path+"{}.html".format(filename)))
    return redirect('/writer/{}'.format(filename))


def get_document(filename):
    filename = secure_filename(filename)
    filename = filename.lower()
    username = get_username()
    try:
        with io.open("userdata/{}/writer/documents/{}.html".format(username, filename), "r", encoding="utf-8") as file:
            document = file.read()
    # except FileNotFoundError:
    #    io.open("text/writerdocs/{}.html".format(name))
    #    document=""
    except IOError:  # Python2
        io.open("userdata/{}/writer/documents/{}.html".format(get_username(), filename), "w")
        refresh_thumbs(username)
        document = ""
    #files = [i for i in files if i.replace("\n", "") != filename+".html"]
    #files.insert(0, filename+".html\n")
    #files=[i.decode("utf-8") for i in files]
    #with io.open('text/writer_file_order.txt', 'w') as file:
    #    file.writelines(files)
    return Markup(document)


