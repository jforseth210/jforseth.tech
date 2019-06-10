from db_tools import get_accounts
from werkzeug.security import generate_password_hash, check_password_hash
#Geez
def check_my_users(user):
    my_users=get_accounts()
    user_data = my_users.get(user['username'])
    if not user_data:
        return False  # <--- invalid credentials
    #Checking if the hash of my password matches the string entered by the user. 
    elif check_password_hash(user_data.get('password'), user['password']):
        return True  # <--- user is logged in!
    return False  # <--- invalid credentials
#I know that these are redundant, but I can't figure out how to pass in arguments in simplelogin. 

def have_access_to_todo(username):
    my_users=get_accounts()
    user_data=my_users.get(username)
    if 'todo' not in user_data.get('has_access_to'):
        return render_template("403.html")
def have_access_to_pickem(username):
    my_users=get_accounts()
    user_data=my_users.get(username)
    if 'pickem' not in user_data.get('has_access_to'):
        return render_template("403.html")
def have_access_to_admin(username):
    my_users=get_accounts()
    user_data=my_users.get(username)
    if 'admin' not in user_data.get('has_access_to'):
        return render_template("403.html")

if __name__ == "__main__":
    print("The function to check user authentication using flask_simplelogin")