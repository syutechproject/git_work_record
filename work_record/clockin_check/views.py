import datetime

from datetime import timedelta
from flask import Blueprint
from flask import render_template
from flask import session
from flask_login import login_required

from work_record.models import get_db


clockin_check = Blueprint('clockin_check', __name__,
                          url_prefix='/work_record/clockin_check')


@clockin_check.route("/check")
@login_required
def check():
    user_id = session.get("user_id")
    clockInHistory = ""
    nowadays = datetime.datetime.now()
    yesterday = nowadays - timedelta(1)
    current_day = nowadays.strftime('%Y-%m-%d')
    yesterday_day = yesterday.strftime('%Y-%m-%d')

    db = get_db()
    cur = db.cursor()

    cur.execute(
        "select * from CLOCKIN_INFO where user_id = '{}' \
            and (clockin_date = '{}'or clockin_date = '{}') \
                order by clockin_date desc, clockin_time desc"
        .format(user_id, current_day, yesterday_day)
    )
    clockInHistory = cur.fetchall()
    cur.close()

    return render_template("clockin_check/check.html", user_id=user_id,
                           clockInHistory=clockInHistory)
