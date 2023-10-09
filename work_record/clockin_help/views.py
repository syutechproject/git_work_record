from flask import Blueprint
from flask_login import login_required
from flask import render_template


clockin_help = Blueprint('clockin_help', __name__,
                         url_prefix='/work_record/clockin_help')


@clockin_help.route("/help")
@login_required
def help():
    return render_template("clockin_help/help.html")
