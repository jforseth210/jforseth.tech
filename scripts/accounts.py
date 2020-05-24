from flask import *
import platform
import os
from flask_simplelogin import get_username
from account_management import *
import secrets
import json
accounts = Blueprint('accounts',__name__)
if os.name=='nt':
    def sh(*args, **kwargs):
        return True
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
            prayerGroups=request.form.get("parishInput")
        if prayerGroups == "":
            prayerGroups="Public"

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
    code=request.args.get('code')
    if check_code(code):
        set_account_validity(username, True)
    else:
        flash("Something went wrong. Try signing in, or email support@jforseth.tech")

    return redirect('/login')
@accounts.route('/account/<account>')
def account(account):
    if account == get_username():
        if platform.node()=="backup-server-vm":
            flash("The main jforseth.tech server is experiencing issues. Password changes and account deletions have been suspended.")
        account=get_account(get_username())
        account.pop("hashed_password")
        return render_template('accounts/account.html',account=account)
    return render_template("errors/403.html"), 403

@accounts.route('/changepw', methods=["GET","POST"])
def change_password():
    old_password=request.form.get("old_password")
    new_password=request.form.get("new_password")
    current_username=get_username()
    current_account=get_account(current_username)
    if platform.node()=="backup-server-vm":
        pass
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
        token=secrets.token_urlsafe(64)
        with open('text/active_reset_tokens.txt') as file:
            reset_dictionary=file.read()
        reset_dictionary=json.loads(reset_dictionary)
        reset_dictionary[token]=username
        reset_dictionary=json.dumps(reset_dictionary)
        with open('text/active_reset_tokens.txt','w') as file:
            file.write(reset_dictionary)
        with open('text/password_reset_email_template.html') as file:
            message=file.read()
        message=message.format(token=token)
        send_email(email,"jforseth.tech password reset",message,PROJECT_EMAIL,PROJECT_PASSWORD)
        flash("If that email/username combination exists, an email with reset instructions will be sent.", category='success')
        return redirect('/')
def check_token(token, delete=False):
        with open('text/active_reset_tokens.txt') as file:
            valid_token_dictionary=file.read()
        valid_token_dictionary=json.loads(valid_token_dictionary)
        return token in valid_token_dictionary
def remove_token(token):
    with open('text/active_reset_tokens.txt') as file:
            valid_token_dictionary=file.read()
    valid_token_dictionary=json.loads(valid_token_dictionary)
    valid_token_dictionary.pop(token)
    valid_token_dictionary=json.dumps(valid_token_dictionary)
    print(valid_token_dictionary)
    with open('text/active_reset_tokens.txt','w') as file:
        file.write(valid_token_dictionary)
def get_user_from_token(token):
    with open('text/active_reset_tokens.txt') as file:
            valid_token_dictionary=file.read()
    valid_token_dictionary=json.loads(valid_token_dictionary)
    return valid_token_dictionary.get(token, "")
@accounts.route('/forgot_pw/reset/<token>', methods=['GET','POST'])
def reset_password(token):
    if request.method=='GET':
        if check_token(token):
            return render_template('accounts/reset.html')
        else:
            flash("Your reset link is invalid. Try again.")
            return redirect('/forgot_pw/reset/{}'.format(token))
    else:
        username=request.form.get('usernameInput')
        new_password=request.form.get('passwordInput')
        if not check_token(token):
            flash("Your reset link is invalid. Try again.")
            return redirect('/forgot_pw/reset/{}'.format(token))
        elif not get_user_from_token(token)==username:
            flash ("Incorrect username.")
            return redirect('/forgot_pw/reset/{}'.format(token))
        else:
            update_pw(username, new_password)
            remove_token(token)
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