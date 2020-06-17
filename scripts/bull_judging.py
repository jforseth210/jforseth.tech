from flask import *

bull_judging = Blueprint("bull_judging", __name__)


@bull_judging.route("/bulljudging")
def bull_judging_homepage():
    return render_template("bull_judging/bulljudginghome.html")


@bull_judging.route("/bulljudging1")
def bull_judging1():
    return render_template("bull_judging/bulljudging1.html")


@bull_judging.route("/bulljudging2")
def bull_judging2():
    return render_template("bull_judging/bulljudging2.html")


@bull_judging.route("/bulljudging3")
def bull_judging3():
    return render_template("bull_judging/bulljudging3.html")


@bull_judging.route("/bulljudging4")
def bull_judging4():
    return render_template("bull_judging/bulljudging4.html")


@bull_judging.route("/bulljudgingdone")
def bull_judging_done():
    return render_template("bull_judging/bulljudgingdone.html")
