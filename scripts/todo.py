from flask import * 
import db_tools
from SensitiveData import *
from simple_mail import send_email
from account_management import have_access_to_todo
from flask_simplelogin import login_required
todo=Blueprint('todo',__name__)# Main page

# The main page
@todo.route('/todo')
@login_required(must=have_access_to_todo)
def todo_page():
    todos = db_tools.get_todos()
    todos = [i.replace('\n', '') for i in todos]
    todos = [i.replace('COMMA', ',') for i in todos]
    todos.reverse()
    return render_template('todo2.html', result=todos)

# Submission route for new todos.
@todo.route('/todo/submitted', methods=['POST', 'GET'])
@login_required(must=have_access_to_todo)
def new_todo():
    name = request.form.get('taskname')
    name = name.replace(',', 'COMMA')
    db_tools.add_todo(name)
    send_email('todo+19z1n4ovd3rf@mail.ticktick.com', name, 'Submitted from jforseth.tech',
                PERSONAL_EMAIL, PERSONAL_PASSWORD)

    return redirect('/todo')

# Deletion route
@todo.route('/todo/delete', methods=['POST', 'GET'])
@login_required(must=have_access_to_todo)
def todo_deleted():
    try:
        task_id = int(request.form.get('taskid'))
    except ValueError:
        return 'Please enter a number...'
    db_tools.delete_todo(task_id)
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
    db_tools.reorder_todo(item_to_reorder, position_to_move)
    return redirect('/todo')