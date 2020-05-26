from flask import *
import platform
import os
from flask_simplelogin import get_username, login_required
from account_management import *
import secrets
import json
from scripts.prayer import PARISH_DICTIONARY
accounts = Blueprint('accounts',__name__)

@accounts.route('/signup', methods=['POST','GET'])
def signup():
    if platform.node()=="backup-server-vm":
         flash("The main jforseth.tech server is experiencing issues. As a result account creation has been temporarily suspended. Please try again later.")
    if request.method == "GET":
        return render_template('accounts/signup.html')
    else:
        email=request.form.get("emailInput")
        username=request.form.get("usernameInput")
        password=request.form.get("passwordInput")
        confirmPassword=request.form.get("confirmPasswordInput")
        prayerBool=request.form.get("prayerInput")
        if not prayerBool:
            prayerGroups='None'
        else:
            prayerGroups=PARISH_DICTIONARY.get(request.form.get("parishInput"), "Public")
            if 'RE' in prayerGroups:
                prayerGroups=prayerGroups+'\n'+prayerGroups.replace('RE','Parish')
        if get_account(username) != {}:
            flash("Account exists already.")
        elif password != confirmPassword:
            flash("Passwords do not match!")
        elif platform.node()=="backup-server-vm":
            pass
        elif len(password) <= 8:
            flash("We've sent a verification email.", category='warning') 
            create_account(username, password, email, prayerGroups, bad_password=True)
        else:
            flash("We've sent a verification email.", category="success")
            create_account(username, password, email, prayerGroups, bad_password=False)
        return redirect('/')

@accounts.route('/validate')
def validate_account():
    username=request.args.get('username')
    token=request.args.get('token')
    if check_token(token, "new_account") and get_user_from_token(token,"new_account") == username:
        set_account_validity(username, True)
        remove_token(token,"new_account")
    else:
        flash("Something went wrong. Try signing in, or email support@jforseth.tech")

    return redirect('/login')

@login_required()
@accounts.route('/account/<account>')
def account(account):
    if account == get_username():
        if platform.node()=="backup-server-vm":
            flash("The main jforseth.tech server is experiencing issues. Password changes and account deletions have been suspended.")
        account=get_account(get_username())
        account.pop("hashed_password")
        return render_template('accounts/account.html',account=account)
    return redirect('/')

@accounts.route('/changepw', methods=["GET","POST"])
def change_password():
    old_password=request.form.get("old_password")
    new_password=request.form.get("new_password")
    confirm_new_password=request.form.get("confirm_new_password")
    current_username=get_username()
    current_account=get_account(current_username)
    if platform.node()=="backup-server-vm":
        pass
    elif new_password != confirm_new_password:
        flash("New passwords do not match!",category="Success")
    elif check_password_hash(current_account.get("hashed_password"), old_password):
        update_pw(current_username, new_password)
        flash("Success!", category="success")
    else:
        flash("Old password incorrect.", category="warning")
    return redirect("/account/{}".format(current_username))

@accounts.route('/forgot_pw', methods=['GET','POST'])
def forgot_pw():
    if request.method=="GET":
        return render_template('accounts/forgot.html')
    else:
        email=request.form.get('emailInput')
        username=request.form.get('usernameInput')
        
        token=generate_token(username, 'password_reset')
        with open('text/password_reset_email_template.html') as file:
            message=file.read()
        message=message.format(token=token)
        send_email(email,"jforseth.tech password reset",message,PROJECT_EMAIL,PROJECT_PASSWORD)
        flash("If that email/username combination exists, an email with reset instructions will be sent.", category='success')
        return redirect('/')

@accounts.route('/forgot_pw/reset/<token>', methods=['GET','POST'])
def reset_password(token):
    if request.method=='GET':
        if check_token(token, "password_reset"):
            return render_template('accounts/reset.html')
        else:
            flash("Your reset link is invalid. Try again.")
            return redirect('/forgot_pw/reset/{}'.format(token))
    else:
        username=request.form.get('usernameInput')
        new_password=request.form.get('passwordInput')
        if not check_token(token,"password_reset"):
            flash("Your reset link is invalid. Try again.")
            return redirect('/forgot_pw/reset/{}'.format(token))
        elif not get_user_from_token(token, "password_reset")==username:
            flash ("Incorrect username.")
            return redirect('/forgot_pw/reset/{}'.format(token))
        else:
            update_pw(username, new_password)
            remove_token(token,"password_reset")
            flash("Password reset sucessfully.",category='success')
            return redirect('/login')

@accounts.route('/accountdel',methods=['POST'])
def account_del():
    password=request.form.get('confirm_password')
    user=get_username()
    current_account=get_account(user)
    if check_password_hash(current_account.get("hashed_password"), password):
        delete_account(user)
        flash("Your account has been deleted!",category="success")
        return redirect('/logout')
    else:
        flash('Incorrect password')
        return redirect('/account/{}'.format(get_username()))