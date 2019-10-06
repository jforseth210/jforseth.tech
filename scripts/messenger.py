from flask import *
import db_tools as db_tools
import time
import pprint #Useful for debug.
pp = pprint.PrettyPrinter(indent=4)

messenger=Blueprint('messenger',__name__)# Main page

@messenger.route('/messenger')
def messenger_main_page():
    messages = db_tools.read_messages()
    messages = [''.join(i) for i in messages]
    return render_template("messenger_main.html", result=messages)

# Shouldn't be necessary any more...
# iframe with messages
# @messenger.route('/messenger/frame')
# def messenger_frame():
#    messages = db_tools.read_messages()
#    messages = [''.join(i) for i in messages]
#    return render_template("messenger_frame.html", result=messages)

# When the user sends a message, it goes here.
@messenger.route('/messenger/result', methods=['POST', 'GET'])
def new_message():
    if request.method == 'POST':
        message = request.form.get('Data')
        db_tools.add_message(message)
    return redirect('/messenger')
@messenger.route('/message/stream')
def message_stream():
    def eventStream():
        previous_messages=db_tools.read_messages()
        while True:
            time.sleep(15)
            messages = db_tools.read_messages()
            if previous_messages != messages:
                previous_messages=messages
                formatted_messages = [''.join(i) for i in messages]
                pp.pprint(formatted_messages)
                yield "data: {}\n\n".format(formatted_messages[-1])
    return Response(eventStream(), mimetype="text/event-stream")
# Clear messages
@messenger.route('/messenger/clear', methods=['POST', 'GET'])
def clear_all_messages():
    db_tools.clear_messages()
    return redirect('/messenger')