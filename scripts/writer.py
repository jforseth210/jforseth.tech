from flask import *
import os
import io
import time
import platform
import os.path
from werkzeug.utils import secure_filename
from SensitiveData import ANDROID_ID
from account_management import have_access_to_writer
from flask_simplelogin import login_required
import refresh_writer_thumbs
writer = Blueprint('writer', __name__)

WRITER_PATH = "text/writerdocs"


@writer.route('/writer')
@login_required(must=have_access_to_writer)
def writer_home():
    if platform.node() == "backup-server-vm":
        flash("The main jforseth.tech server is currently experiencing issues. Your changes may not be saved when the main server comes back online.")
    files = []
    listdir_files = os.listdir(WRITER_PATH)
    listdir_files = [i for i in listdir_files if i!='oopsie']
    with open("text/writer_file_order.txt", "r") as file:
        ordered_files = file.readlines()
    ordered_files = [i.replace("\n", '') for i in ordered_files]
    if len(ordered_files) == len(listdir_files):  # Minus 1 because of the oopsie dir
        print(len(ordered_files))
        print(len(listdir_files))
        print(ordered_files)
        print(listdir_files)
        files = ordered_files
    else:
        additional_files = set(listdir_files).difference(ordered_files)
        for i in additional_files:
            files.insert(0, i)
        print(files)
        files = listdir_files
    new_files = []
    for i in files:
        if i != 'oopsie':
            i = i.replace('.html', "")
            i = i.title()
            new_files.append(i)
    return render_template("writer/writer.html", docs=new_files)


@writer.route('/writer/thumb/<name>')
def writer_thumb(name):
    return send_file('static/writer/thumbs/{}.html_thumb.png'.format(name))


@writer.route('/writer/<name>')
@login_required(must=have_access_to_writer)
def writer_page(name):
    # with io.open("The Healer.html",encoding="utf-8") as file:
    #    document=file.read()
    # document=Markup(document)
    return render_template("writer/Summernote.html", name=name)


@writer.route('/writer/save/<name>', methods=["POST"])
@login_required(must=have_access_to_writer)
def web_save(name):
    data = request.form.get("editordata")
    return save(name, data)


@writer.route("/writer/api/save/<name>", methods=["POST"])
def api_save(name):
    request_id = request.form.get("id")
    data = request.form.get("editordata")
    if request_id == ANDROID_ID:
        save(name, data)
        return ""
    else:
        print(ANDROID_ID, request_id)
        return "Invalid id."


def save(name, data):
    name = secure_filename(name)
    name = name.lower()
    if not os.path.isfile("text/writerdocs/{}.html".format(name)):
        refresh_writer_thumbs()
    with io.open("text/writerdocs/{}.html".format(name), "w", encoding="utf-8") as file:
        document = file.write(data)
    return redirect('/writer/{}'.format(name))


def get_document(name):
    name = secure_filename(name)
    name = name.lower()
    try:
        with io.open("text/writerdocs/{}.html".format(name), "r", encoding="utf-8") as file:
            document = file.read()
    # except FileNotFoundError:
    #    io.open("text/writerdocs/{}.html".format(name))
    #    document=""
    except IOError:  # Python2
        io.open("text/writerdocs/{}.html".format(name), "w")
        refresh_writer_thumbs.main()
        document = ""
    with io.open("text/writer_file_order.txt", "r") as file:
        files = file.readlines()
    files = [i for i in files if i.replace("\n", "") != name+".html"]
    files.insert(0, name+".html\n")
    #files=[i.decode("utf-8") for i in files]
    with io.open('text/writer_file_order.txt', 'w') as file:
        file.writelines(files)
    return Markup(document)


@writer.route('/writer/document/<name>')
@login_required(must=have_access_to_writer)
def document_noapi(name):
    document = get_document(name)
    return document


@writer.route("/writer/api/document/<name>")
def document_api(name):
    request_id = request.args.get("id")
    if request_id == ANDROID_ID:
        requested_document = get_document(name)
        return requested_document
    else:
        print(ANDROID_ID, request_id)
        return "Invalid id."
