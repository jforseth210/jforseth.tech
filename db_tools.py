import sqlite3
import random

###########
#Acccounts#
############
# These are actual logins, with passwords, not just emails!


def get_accounts():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM accounts")
    account_data = cur.fetchall()
    accounts = {}
    for i in account_data:
        username = i[0]
        password = i[1]
        has_access_to = i[2].split(',')

        tempdict = {}
        tempdict.update({'password': password})
        tempdict.update({'has_access_to': has_access_to})
        accounts[username] = tempdict
    return(accounts)

###########
#Messenger#
###########


def add_message(result):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    with conn:
        cur.execute("INSERT INTO messages VALUES(:result)", {'result': result})


def read_messages():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM messages")
    return cur.fetchall()


def clear_messages():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    with conn:
        cur.execute("DELETE FROM messages")
        #Code worked without this line before. Randomly decided to throw an error. ]
        #Googled it, and this line makes the code work again.
        cur.execute("END TRANSACTION")
        cur.execute("VACUUM")
########
#Prayer#
########


def get_verification_code():
    file = open('text/validcodes.txt', 'r')
    validcodes = file.readline()
    file.close()
    randomNum = random.randint(0, len(validcodes)-5)
    code = validcodes[randomNum:randomNum+5]
    return code


def get_verification_email_template():
    file = open('text/verification_email_template.html')
    verification_email = file.read()
    file.close()
    return verification_email


def add_to_mailing_list(address, parish):
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    with conn:
        cur.execute("""INSERT INTO users VALUES(:email,:parish)""",
                    {'email': address, 'parish': parish})


def check_verification_code(code):
    file = open('text/validcodes.txt', 'r')
    validcodes = file.readline()
    return code in validcodes


def read_prayer_request_template(name, prequest, parish):
    file = open("text/prayer_request_email_template.html")
    template = file.read()
    file.close()

    subject = '{} has sent a prayer request to {}'
    subject = subject.format(name, parish)
    message = template.format(name, parish, prequest)

    return(message, subject)


def get_emails_from_parish(parish):
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    with conn:
        cur.execute("""SELECT * FROM users WHERE parish=:parish""",
                    {'parish': parish})
    emails = cur.fetchall()
    emails = [i[0] for i in emails]
    return emails

######
#TODO#
######


def get_todos():
    file = open('text/todo.csv', 'r')
    todos = file.readlines()
    file.close()
    return todos


def add_todo(name):
    file = open('text/todo.csv', 'a')
    file.write('{}\n'.format(name))
    file.close()

def delete_todo(taskid):
    file = open("text/todo.csv", 'r')
    items = file.readlines()
    file.close()
   
    #This line is magic. No idea what's going on. 
    items.pop(len(items)-taskid)

    file = open("text/todo.csv", 'w')
    for i in items:
        file.write(i)
    file.close()

def reorder_todo(item_to_reorder,position_to_move):
        file = open("text/todo.csv", 'r')
        items = file.readlines()
        file.close()
        
        item_to_reorder = items[len(items)-item_to_reorder]
        position_to_move = len(items)-position_to_move
        items.remove(item_to_reorder)
        items.insert(position_to_move, item_to_reorder)
        file = open("text/todo.csv", 'w')
        # Now that the item has been reordered, rewrite the file.
        for i in items:
            file.write(i)
        file.close()
#######
#Admin#
#######
def get_all_from_table(table):
        conn = sqlite3.connect('database.db')
        cur = conn.cursor()
        cur.execute("SELECT * FROM {}".format(table))
        return cur.fetchall()
if __name__ == "__main__":
    print("This is the database management code for jforseth.tech. It is not intended for any other use case.")
