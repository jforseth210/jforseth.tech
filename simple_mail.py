import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(email_recipient, email_subject, email_message, sender, password):
   
    s = smtplib.SMTP(host='smtp.gmail.com', port='587')
    s.starttls()
    s.login(sender, password)
    
    # Create the message
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = email_recipient
    msg['Subject'] = email_subject
   
    msg.attach(MIMEText(email_message, 'html'))

    s.sendmail(msg['From'], msg['To'], msg.as_string())
    del msg
    s.quit()
    
def simple_mail_help():
    print("This is a module for easily sending emails. To use it, import it into your program and call send_email().")
    print("Arguments:")
    print("Email recipient: Who you're sending the email too.")    
    print("Email subject: What the subject line should be.")
    print("Email message: What the message should be. Sent as HTML but works with plaintext.")
    print("Sender: The account to send from. CURRENTLY ONLY WORKS WITH GMAIL.")
    print("Password: The passwords of the account to send from.")
    print("If using a new account, make sure less secure access is turned ON.")

if __name__ == "__main__":
    simple_mail_help()
    
