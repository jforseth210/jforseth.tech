import sqlite3
import random

#All of the data for this site is stored in a local SQLite database except:
#Todos, which are stored in a CSV file.
#Valid codes for verification emails, which are stored in a TXT. 
#Email templates which are stored as HTML. 
#Video data, also a txt. Source code in webtool.py.

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

        temporary_dict = {}
        temporary_dict.update({'password': password})
        temporary_dict.update({'has_access_to': has_access_to})
        
        accounts[username] = temporary_dict
    return(accounts)
########
#Videos#
########
def get_videos():
    # videos.txt is the list of videos
    # It's formatted like this:
    #   The video's title|youtube_id
    #   Another video|youtube_id
    # Note that the youtube id is not the same as the link to the video.
    with open("text/videos.txt", 'r') as file:
        videos = file.readlines()
    return videos
def overwrite_videos(video_list):
    with open('text/videos.txt', 'w') as file:
        file.writelines(video_list)
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
        
        #Broke again, commenting this line out fixed it.
        #I don't know if I need it or not but for the moment it works.
        
        #If something message-related breaks, try toggling this:
        #cur.execute("END TRANSACTION")
        cur.execute("VACUUM")



########
#Prayer#
########


def get_verification_code():
    with open('text/validcodes.txt', 'r') as file:
        VALID_CODES = file.readline()
    random_number = random.randint(0, len(VALID_CODES)-5)
    code = VALID_CODES[random_number:random_number+5]
    return code

def check_verification_code(code):
    with open('text/validcodes.txt', 'r') as file:
            valid_codes = file.readline()

    print("Code:"+code)
    print("Valid Code:"+valid_codes)

    if code in valid_codes:
        code_validity= True
    else:
        code_validity= False
    print("Code Validity:"+str(code_validity))


    new_code = str(random.randint(10000,99999))
    print("New Code:"+new_code)
    valid_codes=valid_codes.replace(code,new_code)
    print("New Valid Code List:"+valid_codes)
    with open('text/validcodes.txt','w') as file:
	    file.write(valid_codes)
    return code_validity

def get_verification_email_template():
    with open('text/verification_email_template.html') as file:
            VERIFICATION_EMAIL_TEMPLATE = file.read()
    return VERIFICATION_EMAIL_TEMPLATE


def add_to_mailing_list(address, parish):
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    with conn:
        cur.execute("""INSERT INTO users VALUES(:email,:parish)""",
                    {'email': address, 'parish': parish})




def read_prayer_request_template(name, prayer_request, parish):
    with open("text/prayer_request_email_template.html") as file:
        PRAYER_REQUEST_TEMPLATE = file.read()

    subject = '{} has sent a prayer request to {}'
    subject = subject.format(name, parish)

    message = PRAYER_REQUEST_TEMPLATE.format(name, parish, prayer_request)

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
    with open('text/todo.csv', 'r') as file:
        todos = file.readlines()
    return todos


def add_todo(name):
    with open('text/todo.csv', 'a') as file:
        file.write('{}\n'.format(name))

def delete_todo(taskid):
    with open("text/todo.csv", 'r') as file:
        todos = file.readlines()
   
    #This line is magic. No idea what's going on. 
    todos.pop(len(todos)-taskid)

    with open("text/todo.csv", 'w') as file:
        for i in todos:
                file.write(i)

def reorder_todo(item_to_reorder,position_to_move):
    with open("text/todo.csv", 'r') as file:
        todos = file.readlines()
            
    item_to_reorder = todos[len(todos)-item_to_reorder]

    position_to_move = len(todos)-position_to_move

    todos.remove(item_to_reorder)
    todos.insert(position_to_move, item_to_reorder)

    with open("text/todo.csv", 'w') as file:
        # Now that the item has been reordered, rewrite the file.
        for i in todos:
            file.write(i)
        
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
