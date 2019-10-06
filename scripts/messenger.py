from flask import *
import sqlite3
import time
import pprint  # Useful for debug.
pp = pprint.PrettyPrinter(indent=4)

messenger = Blueprint('messenger', __name__)  # Main page


def add_message(result):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    with conn:
        cur.execute("INSERT INTO messages VALUES(:result)", {'result': result})


def read_messages():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM messages")
    return cur.fetchall()


def clear_messages():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    with conn:
        cur.execute("DELETE FROM messages")

        # Code worked without this line before. Randomly decided to throw an error. ]
        # Googled it, and this line makes the code work again.

        # Broke again, commenting this line out fixed it.
        # I don't know if I need it or not but for the moment it works.

        # If something message-related breaks, try toggling this:
        #cur.execute("END TRANSACTION")
        cur.execute("VACUUM")


@messenger.route('/messenger')
def messenger_main_page():
    messages = read_messages()
    messages = [''.join(i) for i in messages]
    return render_template("messenger_main.html", result=messages)

# Shouldn't be necessary any more...
# iframe with messages
# @messenger.route('/messenger/frame')
# def messenger_frame():
#    messages = read_messages()
#    messages = [''.join(i) for i in messages]
#    return render_template("messenger_frame.html", result=messages)

# When the user sends a message, it goes here.
@messenger.route('/messenger/result', methods=['POST', 'GET'])
def new_message():
    if request.method == 'POST':
        message = request.form.get('Data')
        add_message(message)
    return redirect('/messenger')


@messenger.route('/message/stream')
def message_stream():
    def eventStream():
        previous_messages = read_messages()
        while True:
            time.sleep(15)
            messages = read_messages()
            if previous_messages != messages:
                previous_messages = messages
                formatted_messages = [''.join(i) for i in messages]
                pp.pprint(formatted_messages)
                yield "data: {}\n\n".format(formatted_messages[-1])
    return Response(eventStream(), mimetype="text/event-stream")
# Clear messages
@messenger.route('/messenger/clear', methods=['POST', 'GET'])
def clear_all_messages():
    clear_messages()
    return redirect('/messenger')
