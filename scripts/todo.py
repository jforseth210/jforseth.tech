import os

from flask import *
from flask_simplelogin import login_required, get_username
from werkzeug.utils import unescape

from SensitiveData import *
from simple_mail import send_email
from account_management import have_access_to_todo

todo = Blueprint("todo", __name__)  # Main page


def get_todos(todoFilePath):
    # try:
    with open(todoFilePath, "r") as file:
        todos = file.readlines()
        if todos != "":
            todos = [i.replace("COMMA", ",") for i in todos]
            todos = [i.replace("\n", "") for i in todos]
            todos = [i.split(",") for i in todos]
    # except FileNotFoundError:
    #    with open(todoFilePath, 'w') as file:
    #        file.write("")
    #        get_todos()
    return todos


def get_lists(todoFilePath):
    todos = get_todos(todoFilePath)
    if todos == "":
        return ""
    lists = [todo[1] for todo in todos]
    lists = list(set(lists))
    return lists


def add_todo(todoFilePath, name, currentlist):
    with open(todoFilePath, "a") as file:
        file.write("{},{}\n".format(name, currentlist))


def delete_todo(todoFilePath, taskid):
    with open(todoFilePath, "r") as file:
        todos = file.readlines()

    # This line is magic. No idea what's going on.
    try:
        todos.pop(len(todos) - taskid)
    except IndexError:
        flash("That isn't a valid task.", category="warning")
        return redirect("/todo")
    with open(todoFilePath, "w") as file:
        for i in todos:
            file.write(i)


def reorder_todo(todoFilePath, item_to_reorder, position_to_move):
    with open(todoFilePath, "r") as file:
        todos = file.readlines()

    item_to_reorder = todos[len(todos) - item_to_reorder]

    position_to_move = len(todos) - position_to_move

    todos.remove(item_to_reorder)
    todos.insert(position_to_move, item_to_reorder)

    with open(todoFilePath, "w") as file:
        # Now that the item has been reordered, rewrite the file.
        for i in todos:
            file.write(i)


# The main page
@todo.route("/todo")
@login_required()
def todo_page():
    # if not os.path.isdir("userdata/{}/todo/".format(get_username().encode('utf-8'))):
    #    os.makedirs('userdata/{}/todo/'.format(get_username().encode('utf-8')))
    #    with open("userdata/{}/todo/list.csv".format(get_username().encode('utf-8')), 'w'):
    #        pass
    todoFilePath = "userdata/{}/todo/list.csv".format(get_username())
    todos = get_todos(todoFilePath)
    todos.reverse()
    lists = get_lists(todoFilePath)
    todos = [(todo[0], todo[1]) for todo in todos]
    lists = [list for list in lists]
    return render_template("todo/todo.html", result=todos, lists=lists)


# Android app and api
"""VALID_DEVICES=[escape(i) for i in VALID_DEVICES]

@todo.route('/todo/api'
    if escape(request.args.get("device")) in VALID_DEVICES:
        todos=get_todos()
        todos.reverse()
        return json.dumps(todos)
    else:
        return "Device not approved"
@todo.route('/todo/submitted/api')
def new_todo_api():
    if escape(request.args.get("device")) in VALID_DEVICES:
        taskname=escape(request.args.get("taskname"))
        taskname,list = taskname.split(',')
        taskname = taskname.replace('COMMA',",")
        list=list.replace("COMMA",",")
        add_todo(taskname,list)
        return ""
    else:
        return "Device not approved"

@todo.route('/todo/delete/api')
def delete_todo_api():
    if escape(request.args.get("device")) in VALID_DEVICES:
        task_id = int(escape(request.args.get('taskid'))) #Shouldn't be necessary, but just in case.
        delete_todo(task_id)
        return ""
    else:
        return "Device not approved"
"""
# Submission route for new todos.
@todo.route("/todo/submitted", methods=["POST", "GET"])
@login_required()
def new_todo():
    todoFilePath = "userdata/{}/todo/list.csv".format(get_username())
    name = request.form.get("taskname")  # Not esaping this because reasons.
    name = name.replace(",", "COMMA")
    currentlist = escape(request.form.get("list"))
    add_todo(todoFilePath, name, currentlist)
    # send_email('todo+19z1n4ovd3rf@mail.ticktick.com', name, 'Submitted from jforseth.tech',PERSONAL_EMAIL, PERSONAL_PASSWORD)

    return redirect("/todo")


# Deletion route
@todo.route("/todo/delete", methods=["POST", "GET"])
@login_required()
def todo_deleted():
    todoFilePath = "userdata/{}/todo/list.csv".format(get_username())
    try:
        task_id = int(escape(request.form.get("taskid")))
    except ValueError:
        flash("Please enter a number", category="warning")
        return redirect("/todo")
    delete_todo(todoFilePath, task_id)
    return redirect("/todo")


# Ordering route
@todo.route("/todo/reorder", methods=["POST", "GET"])
@login_required()
def todo_reordered():
    todoFilePath = "userdata/{}/todo/list.csv".format(get_username())
    try:
        item_to_reorder = int(escape(request.form.get("taskid")))
        position_to_move = int(escape(request.form.get("taskloc")))
    except ValueError:
        flash("Please enter a number", category="warning")
    reorder_todo(todoFilePath, item_to_reorder, position_to_move)
    return redirect("/todo")
