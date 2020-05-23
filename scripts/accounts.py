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
    with open('text/validcodes.txt', 'r') as file:
        valid_codes = file.readline()

    if code in valid_codes:
        set_account_validity(username, True)
    else:
        flash("Something went wrong. Try signing in, or email support@jforseth.tech")
    new_code = str(random.randint(10000, 99999))
    print("New Code:"+new_code)
    valid_codes = valid_codes.replace(code, new_code)
    print("New Valid Code List:"+valid_codes)
    with open('text/validcodes.txt', 'w') as file:
        file.write(valid_codes)
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
@accounts.route('/accountdel')
def account_del():
    user=get_username()
    delete_account(user)
    flash("Your account has been deleted!",category="success")
    return redirect('/logout')