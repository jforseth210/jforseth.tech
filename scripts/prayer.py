import platform
import random
import pprint  # Useful for debug.

from flask import *
import sqlite3
from flask_simplelogin import login_required, get_username

from simple_mail import send_email
from account_management import generate_token, check_token, remove_token, get_user_from_token
from SensitiveData import *

pp = pprint.PrettyPrinter(indent=4)

prayer = Blueprint('prayer', __name__)
# This is a dictionary that converts the code the user typed in into a parish.
# If adding a new group:
# REMEMBER TO UPDATE THE HTML
PARISH_DICTIONARY = {
    'Public': 'Public',
    'STJOHNRE': 'Saint John RE',
    'STJOHN': 'Saint John Parish',
    'STJOSEPH': 'Saint Joseph Parish',
    'STJOSEPHRE': 'Saint Joseph RE',
    # 'FFTEACHERS': 'Fairfield Catholic Teachers',
    'JESUS': 'LL Small Group 3',
    'MT4H': "State Award Demo",
    # There shouldn't be any way to sign up for testing group.
    "sdkfjglhgjnfkbsdnfbjgksdngfkjngkfdsgjksdgjbak": "Testing",
    "BRANDNEW": "Signup Tests"
}
enter_tests_into_db = False

# Email verification


def get_verification_code():
    with open('text/validcodes.txt', 'r') as file:
        VALID_CODES = file.readline()
    random_number = random.randint(0, len(VALID_CODES)-5)
    code = VALID_CODES[random_number:random_number+5]
    return code


def get_verification_email_template():
    with open('text/verification_email_template.html') as file:
        VERIFICATION_EMAIL_TEMPLATE = file.read()
    return VERIFICATION_EMAIL_TEMPLATE


def check_verification_code(code):
    with open('text/validcodes.txt', 'r') as file:
        valid_codes = file.readline()

    print("Code:"+code)
    print("Valid Code:"+valid_codes)

    if code in valid_codes:
        code_validity = True
    else:
        code_validity = False
    print("Code Validity:"+str(code_validity))

    new_code = str(random.randint(10000, 99999))
    print("New Code:"+new_code)
    valid_codes = valid_codes.replace(code, new_code)
    print("New Valid Code List:"+valid_codes)
    with open('text/validcodes.txt', 'w') as file:
        file.write(valid_codes)
    return code_validity


def add_to_mailing_list(address, parishes):
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    parishstring = "\n".join(parishes)
    if address != "testing@jforseth.tech" and not enter_tests_into_db:
        with conn:
            cur.execute("""INSERT INTO users VALUES(:email,:parish)""",
                        {'email': address, 'parish': parishstring})
    else:
        print("This is the testing email. If you used a normal email, these values would've been added: \nEmail=" +
              address+"\nParishes="+parishes)
# Prayer request submissions


def read_prayer_request_template(email, name, prayer_request, parish):
    with open("text/prayer_request_email_template.html") as file:
        PRAYER_REQUEST_TEMPLATE = file.read()

    subject = '{} has sent a prayer request to {}'
    subject = subject.format(name, parish)

    message = PRAYER_REQUEST_TEMPLATE.format(
        email=email, name=name, group=parish, request=prayer_request)

    return(message, subject)


def get_emails_from_parish(parish):
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    with conn:
        cur.execute(
            """SELECT prayer_email FROM accounts WHERE prayer_groups LIKE '%{}%'""".format(parish))
    emails = cur.fetchall()

    return emails
# The main page
@prayer.route('/prayer')
def prayer_page():
    if platform.node() == "backup-server-vm":
        flash("The jforseth.tech main server is experiencing issues. Emails may fail to send and new accounts may not be saved.")
    return render_template('prayer/prayer.html', options=PARISH_DICTIONARY.values())


@prayer.route('/FlaskApp/prayer')
def old_prayer_page():
    return redirect('/prayer')


@prayer.route('/prayer/prayerrequest', methods=['POST', 'GET'])
def prayer_request():
    name = escape(request.form.get('name'))
    prequest = escape(request.form.get('prequest'))
    parish = escape(request.form.get('parish'))

    emails = get_emails_from_parish(parish)

    message_template, subject_template = read_prayer_request_template("EMAIL_PLACEHOLDER",
                                                                      name, prequest, parish)

    # For testing purposes only, manually overrides email list and sends to my personal account instead:
    # Uncommenting this is a really, really bad idea.
    # emails=[personalemail]
    for email in emails:
        # This token generation is a bit hacky because I don't know the username. But, if I don't check on the other side, it doesn't matter anyway.
        send_email(email[0], subject_template, message_template.format(email=email[0]),
                   PROJECT_EMAIL, PROJECT_PASSWORD)
    flash("Prayer request sent!", category="success")
    return redirect('/prayer')


@prayer.route('/prayer/unsub')
def confirm_unsubscription():
    email = escape(request.args.get('email'))
    group = escape(request.args.get('group'))
    token = generate_token(email, 'prayer_unsubscription')
    with open('text/prayer_unsubscription_email_template.html') as file:
        message = file.read()
    message = message.format(email=email, group=group, token=token)
    if group == "ALL":
        group = "all prayer requests."
    send_email(email, "Unsubscribe from "+group,
               message, PROJECT_EMAIL, PROJECT_PASSWORD)
    flash("Sorry to see you go! Check your email for an unsubscription link.",
          category='success')
    return redirect('/prayer')


@prayer.route('/prayer/unsub_confirmed')
def unsubscribe_page():
    email = escape(request.args.get('email'))
    group = escape(request.args.get('group'))
    token = escape(request.args.get('token'))
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    if check_token(token, 'prayer_unsubscription') and get_user_from_token(token, 'prayer_unsubscription') == email:
        with conn:
            cur.execute(
                """SELECT prayer_groups, username FROM accounts WHERE prayer_email='{email}'""".format(email=email))
        users = cur.fetchall()
        if group != "ALL":
            for idx, user in enumerate(users):
                user=list(user)
                user[0] = user[0].replace(group, "")
                user[0] = user[0].strip('|')
                user[0] = user[0].replace('||', '|')
                if user[0] == "":
                    users[idx] = ("None", user[1])
                else:
                    users[idx] = (user[0], user[1])
        else:
            users = [("None", user[1]) for user in users]
        with conn:
            for user in users:
                cur.execute(
                    """UPDATE accounts SET prayer_groups = ? WHERE username = ?""", (user[0], user[1]))
        remove_token(token, 'prayer_unsubscription')
        flash("Done", category="success")
    else:
        flash("This link is invalid.")
    return redirect('/prayer')


@login_required()
@prayer.route('/prayer/unsubscribe_logged_in')
def unsubscribe_logged_in():
    username = get_username()
    group = escape(request.args.get('group'))
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    with conn:
        cur.execute(
            """SELECT prayer_groups FROM accounts WHERE username = ? """, ([username]))
    prayer_groups = cur.fetchone()[0]
    prayer_groups = prayer_groups.replace(group, "")
    prayer_groups = prayer_groups.strip('|')
    prayer_groups = prayer_groups.replace('||', '|')
    if prayer_groups == '':
        prayer_groups = "None"
    print(prayer_groups)
    with conn:
        cur.execute("""UPDATE accounts SET prayer_groups = ? WHERE username= ?""", ([
                    prayer_groups, username]))
    flash('Unsubscribed', category='success')
    return redirect('/account/'+username)


@prayer.route('/prayer/addgroup', methods=['POST'])
def add_group():
    group = escape(request.form.get('group'))
    username = get_username()
    group = PARISH_DICTIONARY.get(group)
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    with conn:
        cur.execute(
            """SELECT prayer_groups FROM accounts WHERE username = ? """, ([username]))
    prayer_groups = cur.fetchone()[0]
    print(prayer_groups)
    if prayer_groups == 'None':
        prayer_groups = group+'|Public'
        flash('Subscribed', category='success')
    elif group in prayer_groups:
        flash("Already part of this group")
    else:
        prayer_groups = prayer_groups+"|"+group
        flash('Subscribed', category='success')

    with conn:
        cur.execute("""UPDATE accounts SET prayer_groups = ? WHERE username= ?""", ([
                    prayer_groups, username]))
    return redirect('/account/'+username)
# @prayer.route('/prayer/newemail', methods=['POST', 'GET'])
# def new_email():
#     if request.method == 'POST':
#         email = escape(request.form.get('email'))
#         parish = escape(request.form.get('parish'))
#         parish = parish.upper()

#         # Takes the parish code, looks it up in the dictionary.
#         # If it's blank or incorrect, replace with "Public"
#         email_parish = PARISH_DICTIONARY.get(parish, "Public")

#         valid_code = get_verification_code()

#         message = get_verification_email_template()
#         message = message.format(
#             parish=email_parish, code=valid_code, email=email)

#         # Sends the adapted message
#         print(email)
#         send_email(
#             email, "Thank you for joining JMJprayerrequests", message, PROJECT_EMAIL, PROJECT_PASSWORD)
#         # Displays a page with further instruction
#         flash("We've sent a verification code to your email.",category="success")
#         return redirect('/prayer')

# # The second step of verification
# # This uses get instead of post in hopes of greater
# # compatibility with email clients.

# @prayer.route('/prayer/newemailconfirmed')
# def new_email_confirmed():
#     code = escape(request.args.get('code'))
#     address = escape(request.args.get('email'))
#     parish = escape(request.args.get('parish'))
#     if len(code) == 0:
#         return("""No verification code was recieved. Please try again.
#         Theres two reasons why this could've happened: <ol>
#         <li>I messed up something with the code.</li>
#         <li>You messed with something you weren't supposed to.</li></ol>
#         </li>If you happen to be me, it's probably both. If you aren't me, feel free to email me if you think it's broken, or to try again if you think you broke it.
#         If problem persists, send me an email describing the problem. <br / >
#         <br/><img src='https://imgs.xkcd.com/comics/unreachable_state.png'/>""")
#     try:
#         verification_result = check_verification_code(code)
#     except TypeError:
#         return """<html><p>Verification Failed. Your email client may not be supported. Try a different client, e.g. Outlook, your email provider's website, the mail prayer on your phone, etc.</p>
#                     <br/><img src='https://imgs.xkcd.com/comics/unreachable_state.png'/></html>"""

#     if verification_result:  # If verification succeeds:
#         #print(parish)
#         #print("Public")
#         #print("If this is true, your code is working:")
#         #print(parish=="Public")
#         #print("RE to Parish:"+parish.replace('RE','Parish'))
#         #Adds email to applicable groups
#         parishes=["Public"]
#         if parish != "Public":
#             parishes.append(parish)
#         if "RE" in parish:
#             parishes.append(parish.replace('RE', 'Parish'))
#         print(parishes)
#         add_to_mailing_list(address, parishes)

#         # Returns success page.
#         flash("You've been added to the following groups: " + ", ".join(parishes),category="success")
#         return redirect('/prayer')
#     else:
#         # Returns failure message.
#         flash("Verification failed. Try again or report the problem.", category="alert")
#         return redirect("/prayer")
