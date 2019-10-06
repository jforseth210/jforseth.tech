from flask import *
import db_tools
from simple_mail import send_email
from SensitiveData import *
import pprint #Useful for debug.
pp = pprint.PrettyPrinter(indent=4)

prayer=Blueprint('prayer',__name__)# Main page

# The main page
@prayer.route('/prayer')
def prayer_page():
    return render_template('prayer.html')

@prayer.route('/FlaskApp/prayer')
def old_prayer_page():
    return redirect('/prayer')

# Email submissions
@prayer.route('/prayer/newemail', methods=['POST', 'GET'])
def new_email():
    if request.method == 'POST':
        email = request.form.get('email')
        parish = request.form.get('parish')
        parish = parish.upper()

        # This is a dictionary that converts the code the user typed in into a parish.
        # If adding a new group:
        # REMEMBER TO UPDATE THE HTML
        parish_dictionary = {
            'STJOHNRE': 'Saint John RE',
            'STJOHN': 'Saint John Parish',
            'STJOSEPH': 'Saint Joseph Parish',
            'STJOSEPHRE': 'Saint Joseph RE',
            'FFTEACHERS': 'Fairfield Catholic Teachers',
            'JESUS': 'LL Small Group 3'
        }

        # Takes the parish code, looks it up in the dictionary.
        # If it's blank or incorrect, replace with "Public"
        email_parish = parish_dictionary.get(parish, "Public")
        valid_code = db_tools.get_verification_code()
        message = db_tools.get_verification_email_template()
        message = message.format(
            email_parish, valid_code, email, email_parish)

        # Sends the adapted message
        send_email(
            email, "Thank you for joining JMJprayerrequests", message, PROJECT_EMAIL, PROJECT_PASSWORD)
        # Displays a page with further instruction
        return render_template('email_adding.html')

# The second step of verification
# This uses get instead of post in hopes of greater
# compatibility with email clients.
@prayer.route('/prayer/newemailconfirmed')
def new_email_confirmed():
    code = request.args.get('code')
    address = request.args.get('email')
    parish = request.args.get('parish')
    if len(code)==0:
        return("""No verification code was recieved. Please try again.
        Theres two reasons why this could've hprayerened: <ol>
        <li>I messed up something with the code.</li>
        <li>You messed with something you weren't supposed to.</li></ol>
        </li>If you hprayeren to be me, it's probably both. If you aren't me, feel free to email me if you think it's broken, or to try again if you think you broke it.
        If problem persists, send me an email describing the problem. <br / >
        <br/><img src='https://imgs.xkcd.com/comics/unreachable_state.png'/>""")
    try:
        verification_result = db_tools.check_verification_code(code)
    except TypeError:
        return """<html><p>Verification Failed. Your email client may not be supported. Try a different client, e.g. Outlook, your email provider's website, the mail prayer on your phone, etc.</p>
                    <br/><img src='https://imgs.xkcd.com/comics/unreachable_state.png'/></html>"""

    if verification_result:  # If verification succeeds:
        # Adds email to prayerlicable groups
        db_tools.add_to_mailing_list(address, parish)
        db_tools.add_to_mailing_list(address, "Public")
        if "RE" in parish:
            new_parish = parish.replace('RE', 'Parish')
            db_tools.add_to_exiymailing_list(address, new_parish)

        # Returns success page.
        return render_template('email_added.html')
    else:
        # Returns failure message.
        return """Email verification failed. Verification code is invalid or expired. Please try signing up again.
        If the problem persists, click "Contact" and send me an email describing your issue. Sorry!"""

# Prayer request submissions
@prayer.route('/prayer/prayerrequest', methods=['POST', 'GET'])
def prayer_request():
    name = request.form.get('name')
    prequest = request.form.get('prequest')
    parish = request.form.get('parish')

    emails = db_tools.get_emails_from_parish(parish)
    message_template, subject_template = db_tools.read_prayer_request_template(
        name, prequest, parish)

    # For testing purposes only, manually overrides email list and sends to my personal account instead:
    # Uncommenting this is a really, really bad idea.
    # emails=[personalemail]

    for email in emails:
        send_email(email, subject_template, message_template,
                    PROJECT_EMAIL, PROJECT_PASSWORD)
    return render_template('sent.html')