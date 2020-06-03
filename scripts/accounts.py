import os
import platform
import json

import secrets
from flask import *
from flask_simplelogin import get_username, login_required

from account_management import *
from scripts.prayer import PARISH_DICTIONARY
accounts = Blueprint('accounts', __name__)

#The initial signup page.
@accounts.route('/signup', methods=['POST', 'GET'])
def signup():
    # The page.
    if request.method == "GET":
        # Don't allow signups on the backup server.
        if platform.node() == "backup-server-vm":
            flash("The main jforseth.tech server is experiencing issues. As a result account creation has been temporarily suspended. Please try again later.")
        return render_template('accounts/signup.html')
    #The form
    else:
        email = escape(request.form.get("emailInput"))
        username = escape(request.form.get("usernameInput"))
        password = escape(request.form.get("passwordInput"))
        confirmPassword = escape(request.form.get("confirmPasswordInput"))
        prayerBool = escape(request.form.get("prayerInput"))
        # The user doesn't want to recieve any prayer requests.
        if not prayerBool:
            prayerGroups = 'None'
        else:
            #User wants prayer requests, but doesn't supply a code.
            #This doesn't need to be escaped, since it'll be checked against a dictionary anyway.
            prayerGroups = PARISH_DICTIONARY.get(
                request.form.get("parishInput"), "Public")

            #RE members should also be signed up for their parishes.
            if 'RE' in prayerGroups:
                prayerGroups = prayerGroups+'|' + \
                    prayerGroups.replace('RE', 'Parish')

        if get_account(username) != {}:
            flash("Account exists already.")

        elif password != confirmPassword:
            flash("Passwords do not match!")

        # If this is the backup server, do nothing.
        elif platform.node() == "backup-server-vm":
            pass
        # Sign the user up, but warn them to change their password in the verification email.
        elif len(password) <= 8:
            flash("We've sent a verification email.", category='warning')
            create_account(username, password, email,
                           prayerGroups, bad_password=True)
        # Sign the user up.
        else:
            flash("We've sent a verification email.", category="success")
            create_account(username, password, email,
                           prayerGroups, bad_password=False)
        return redirect('/')

#The link in the validation email.
@accounts.route('/validate')
def validate_account():
    username = escape(request.args.get('username'))
    token = escape(request.args.get('token'))
    #Check that the token is valid, and has been issued to this user.
    if check_token(token, "new_account") and get_user_from_token(token, "new_account") == username:
        #Validate the account and deactivate the token.
        set_account_validity(username, True)
        remove_token(token, "new_account")
    else:
        flash("Something went wrong. Try signing in, or email support@jforseth.tech")

    return redirect('/login')

# The account page.
@login_required()
@accounts.route('/account/<account>')
def account(account):
    if account.encode('utf-8') == get_username().encode('utf-8'):
        if platform.node() == "backup-server-vm":
            flash("The main jforseth.tech server is experiencing issues. Account changes have been suspended.")
        account = get_account(get_username().encode('utf-8'))
        groups = account['prayer_groups'].split('|')
        return render_template('accounts/account.html', groups=groups)
    return redirect('/')

#The change password form
@accounts.route('/changepw', methods=["GET", "POST"])
def change_password():
    old_password = escape(request.form.get("old_password"))
    new_password = escape(request.form.get("new_password"))
    confirm_new_password = escape(request.form.get("confirm_new_password"))

    current_username = get_username().encode('utf-8')
    current_account = get_account(current_username)

    if platform.node() == "backup-server-vm":
        pass

    elif new_password != confirm_new_password:
        flash("New passwords do not match!", category="Success")

    elif check_password_hash(current_account.get("hashed_password"), old_password):
        update_pw(current_username, new_password)
        flash("Success!", category="success")

    else:
        flash("Old password incorrect.", category="warning")

    return redirect("/account/{}".format(current_username))

#Email change form. Basically just sends an email.
@accounts.route('/change_email', methods=['POST'])
def verify_changed_email():
    email = escape(request.form.get('email'))
    email_type = escape(request.form.get('email_type'))

    username = get_username().encode('utf-8')
    token = generate_token(email+username, 'email_change')

    with open('text/change_email_template.html') as file:
        message = file.read()
    message = message.format(
        username=username, email=email, email_type=email_type, token=token)
    send_email(email, "Change your "+email_type.lower(),
               message, PROJECT_EMAIL, PROJECT_PASSWORD)
    flash("We've sent a verification link to that email address.", category='success')
    return redirect('/account/'+username)

#Actually change the email.
#Validation link from the email.
@accounts.route('/change_email/verified')
def change_email_page():
    token = escape(request.args.get("token"))
    username = escape(request.args.get("username"))
    email_type = escape(request.args.get("type"))
    email = escape(request.args.get("email"))

    EMAIL_TYPES = {
        'Recovery email': 'recovery_email',
        'Prayer email': 'prayer_email'
    }

    if check_token(token, 'email_change') and get_user_from_token(token, 'email_change') == email+username:
        email_type = EMAIL_TYPES.get(email_type)
        change_email(username, email, email_type)
        remove_token(token, 'email_change')
        flash("Success!", category='success')
        return redirect('/account/'+username)

    else:
        flash("That link didn't work, try again.")
        return redirect('/account/'+username)


@accounts.route('/forgot_pw', methods=['GET', 'POST'])
def forgot_pw():
    if request.method == "GET":
        return render_template('accounts/forgot.html')
    else:
        email = escape(request.form.get('emailInput'))
        username = escape(request.form.get('usernameInput'))

        token = generate_token(username, 'password_reset')
        with open('text/password_reset_email_template.html') as file:
            message = file.read()
        message = message.format(token=token)
        send_email(email, "jforseth.tech password reset",
                   message, PROJECT_EMAIL, PROJECT_PASSWORD)
        flash("If that email/username combination exists, an email with reset instructions will be sent.", category='success')
        return redirect('/')


@accounts.route('/forgot_pw/reset/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if request.method == 'GET':
        if check_token(token, "password_reset"):
            return render_template('accounts/reset.html')
        else:
            flash("Your reset link is invalid. Try again.")
            return redirect('/forgot_pw/reset/{}'.format(token))
    else:
        username = escape(request.form.get('usernameInput'))
        new_password = escape(request.form.get('passwordInput'))
        if not check_token(token, "password_reset"):
            flash("Your reset link is invalid. Try again.")
            return redirect('/forgot_pw/reset/{}'.format(token))
        elif not get_user_from_token(token, "password_reset") == username:
            flash("Incorrect username.")
            return redirect('/forgot_pw/reset/{}'.format(token))
        else:
            update_pw(username, new_password)
            remove_token(token, "password_reset")
            flash("Password reset sucessfully.", category='success')
            return redirect('/login')


@accounts.route('/accountdel', methods=['POST'])
def account_del():
    password = escape(request.form.get('confirm_password'))
    user = get_username().encode('utf-8')
    current_account = get_account(user)
    if check_password_hash(current_account.get("hashed_password"), password):
        delete_account(user)
        flash("Your account has been deleted!", category="success")
        return redirect('/logout')
    else:
        flash('Incorrect password')
