from flask import *
import platform
import os
from flask_simplelogin import get_username
from account_management import *
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
        print(get_account(username))
        if get_account(username) != {}:
            flash("Account exists already.")
        elif password != confirmPassword:
            flash("Passwords do not match!")
        elif platform.node()=="backup-server-vm":
            pass
        elif len(password) <= 8:
            flash("Account created, do you want to login and choose a more secure password?", category='warning') 
            create_account(username, password)
        else:
            flash("Account created, login to access.", category="success")
            create_account(username, password)
        return redirect('/login?next=%2Faccount%2F'+username)
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
@accounts.route('/accountdel')
def account_del():
    user=get_username()
    delete_account(user)
    flash("Your account has been deleted!",category="success")
    return redirect('/logout')