from flask import *
from SensitiveData import *
from simple_mail import send_email
from account_management import have_access_to_todo
from flask_simplelogin import login_required
todo = Blueprint('todo', __name__)  # Main page


def get_todos():
    with open('text/todo.csv', 'r') as file:
        todos = file.readlines()
    return todos


def add_todo(name):
    with open('text/todo.csv', 'a') as file:
        file.write('{}\n'.format(name))


def delete_todo(taskid):
    with open("text/todo.csv", 'r') as file:
        todos = file.readlines()

    # This line is magic. No idea what's going on.
    try:
        todos.pop(len(todos)-taskid)
    except IndexError:
        return "That isn't a valid task."
    with open("text/todo.csv", 'w') as file:
        for i in todos:
            file.write(i)


def reorder_todo(item_to_reorder, position_to_move):
    with open("text/todo.csv", 'r') as file:
        todos = file.readlines()

    item_to_reorder = todos[len(todos)-item_to_reorder]

    position_to_move = len(todos)-position_to_move

    todos.remove(item_to_reorder)
    todos.insert(position_to_move, item_to_reorder)

    with open("text/todo.csv", 'w') as file:
        # Now that the item has been reordered, rewrite the file.
        for i in todos:
            file.write(i)

# The main page
@todo.route('/todo')
@login_required(must=have_access_to_todo)
def todo_page():
    todos = get_todos()
    todos = [i.replace('\n', '') for i in todos]
    todos = [i.replace('COMMA', ',') for i in todos]
    todos.reverse()
    return render_template('todo2.html', result=todos)
@todo.route('/todo/api')
def todo_api():
    if request.args.get("device") in VALID_DEVICES:
        return json.dumps(get_todos().reverse())
    else:
        return "Device not approved"
@todo.route('/todo/submitted/api')
def new_todo_api():
    if request.args.get("device") in VALID_DEVICES:
        taskname=request.args.get("taskname")
        taskname = taskname.replace(',', 'COMMA')
        add_todo(taskname)
    else:
        return "Device not approved"

@todo.route('/todo/delete/api')
def delete_todo_api():
    if request.arg.get("device") in VALID_DEVICES:
        task_id = int(request.form.get('taskid'))
        delete_todo(task_id)
# Submission route for new todos.
@todo.route('/todo/submitted', methods=['POST', 'GET'])
@login_required(must=have_access_to_todo)
def new_todo():
    name = request.form.get('taskname')
    name = name.replace(',', 'COMMA')
    add_todo(name)
    #send_email('todo+19z1n4ovd3rf@mail.ticktick.com', name, 'Submitted from jforseth.tech',PERSONAL_EMAIL, PERSONAL_PASSWORD)

    return redirect('/todo')

# Deletion route
@todo.route('/todo/delete', methods=['POST', 'GET'])
@login_required(must=have_access_to_todo)
def todo_deleted():
    try:
        task_id = int(request.form.get('taskid'))
    except ValueError:
        return 'Please enter a number...'
    delete_todo(task_id)
    return redirect('/todo')

# Ordering route
@todo.route('/todo/reorder', methods=['POST', 'GET'])
@login_required(must=have_access_to_todo)
def todo_reordered():
    try:
        item_to_reorder = int(request.form.get("taskid"))
        position_to_move = int(request.form.get("taskloc"))
    except ValueError:
        return 'Please enter a number...'
    reorder_todo(item_to_reorder, position_to_move)
    return redirect('/todo')
