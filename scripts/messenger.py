import time
import pprint  # Useful for debug.
import sys
import sqlite3

from flask import *

pp = pprint.PrettyPrinter(indent=4)

messenger = Blueprint("messenger", __name__)  # Main page


def add_message(result):
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    with conn:
        cur.execute("INSERT INTO messages VALUES(:result)", {"result": result})


def read_messages():
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM messages")
    return cur.fetchall()


def clear_messages():
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    with conn:
        cur.execute("DELETE FROM messages")
        if sys.version_info[0] == 3:
            cur.execute("END TRANSACTION")
        #cur.execute("VACUUM")


@messenger.route("/messenger")
def messenger_main_page():
    messages = read_messages()
    messages = ["".join(i) for i in messages]
    return render_template("messenger/messenger.html", result=messages)


# When the user sends a message, it goes here.
@messenger.route("/messenger/result", methods=["POST", "GET"])
def new_message():
    if request.method == "POST":
        message = escape(request.form.get("message"))
        add_message(message)

    return redirect("/messenger")


@messenger.route("/message/stream")
def message_stream():
    def eventStream():
        previous_messages = read_messages()
        while True:
            time.sleep(10)
            messages = read_messages()

            if previous_messages != messages:
                previous_messages = messages
                formatted_messages = ["".join(i) for i in messages]

                yield "data: {}\n\n".format(formatted_messages[-1])

    return Response(eventStream(), mimetype="text/event-stream")


@messenger.route("/messenger/clear", methods=["POST", "GET"])
def clear_all_messages():
    clear_messages()
    return redirect("/messenger")
