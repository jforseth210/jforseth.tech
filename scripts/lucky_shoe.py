from flask import *
from twilio.rest import Client
from simple_mail import send_email
from SensitiveData import *
lucky_shoe = Blueprint('lucky_shoe', __name__)  # Main page

@lucky_shoe.route('/luckyshoe')
def lucky_shoe_home():
    return render_template('lucky_shoe/luckyshoe.html')
@lucky_shoe.route('/luckyshoe/formtemplates')
def lucky_shoe_form_templates():
    return render_template('lucky_shoe/form_templates.html')
@lucky_shoe.route('/luckyshoe/order', methods=["POST"])
def lucky_shoe_order():
    rq=request.form.to_dict()
    paramlist=[]
    for key, val in rq.items():
        paramlist.append("{}: {}".format(key, val))
    paramlist="<br />".join(paramlist)
    send_email("dinodigger210@gmail.com","New Horseshoe Order", paramlist, PROJECT_EMAIL,PROJECT_PASSWORD) 
    flash("Order submitted sucessfully.", category="success")



    # Your Account Sid and Auth Token from twilio.com/console
    # DANGER! This is insecure. See http://twil.io/secure
    account_sid = TWILIO_SID
    auth_token = TWILIO_TOKEN
    client = Client(account_sid, auth_token)

    message = client.messages \
                    .create(
                        body="JForseth.tech: Horseshoe Order",
                        from_='+12564190477',
                        to=NOLAN_NUMBER
                    )

    return redirect("/luckyshoe")