from flask import *
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
    send_email("luckyshoe@jforseth.tech","New Horseshoe Order", paramlist, PROJECT_EMAIL,PROJECT_PASSWORD) 
    flash("Order submitted sucessfully.", category="success")
    return redirect("/luckyshoe")