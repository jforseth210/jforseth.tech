from flask import *
lucky_shoe = Blueprint('lucky_shoe', __name__)  # Main page

@lucky_shoe.route('/luckyshoe')
def lucky_shoe_home():
    return render_template('lucky_shoe/luckyshoe.html', PRICE="PRICE PLACEHOLDER")