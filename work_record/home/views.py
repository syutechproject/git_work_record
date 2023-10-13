import datetime
import logging

from datetime import timedelta
from flask import Blueprint
from flask import render_template
from flask import request
from flask import session
from flask_login import login_required

from work_record.models import get_db


home = Blueprint('home', __name__, url_prefix='/work_record/home')


def sql_select(user_id, clockin_div, yyyy_mm_dd, cur):
    CLOCKIN_DIV = {"start": "1", "finish": "2", "stop": "3", "resume": "4"}
    logging.warning(
        "#########" + CLOCKIN_DIV[clockin_div] + "select SQL Start#########")

    cur.execute(
        "select max(serno) from CLOCKIN_INFO \
            where user_id = '{}' and clockin_div='{}' and clockin_date =  '{}'"
        .format(user_id, CLOCKIN_DIV[clockin_div], yyyy_mm_dd)
    )
    sqlResult = cur.fetchone()

    return sqlResult


def sql_insert(user_id, clockin_div, yyyy_mm_dd, strSerno, hh_mm_ss, cur):
    CLOCKIN_DIV = {"start": "1", "finish": "2", "stop": "3", "resume": "4"}
    logging.warning(
        "#########" + CLOCKIN_DIV[clockin_div] + "insert SQL Start#########")
    logging.warning("#####yyyy_mm_dd=" + yyyy_mm_dd + "######")
    logging.warning("#####hh_mm_ss" + hh_mm_ss + "######")
    sqlResult = cur.execute(
        "insert into CLOCKIN_INFO \
            (user_id, clockin_date, clockin_div, serno, clockin_time) \
                values('{}', '{}', '{}', '{}', '{}')"
        .format(user_id, yyyy_mm_dd, CLOCKIN_DIV[clockin_div], strSerno,
                hh_mm_ss)
    )
    return sqlResult


@home.route('/', methods=['GET', 'POST'])
@login_required
def work_record():
    error_message = ''
    db = get_db()
    cur = db.cursor()
    user_id = session.get("user_id")
    logging.warning(user_id)

    nowDate = datetime.datetime.now()
    logging.warning("####nowDate####")
    logging.warning(nowDate)
    now_hour = nowDate.hour
    now_minute = nowDate.minute
    now_second = nowDate.second
    str_hh_mm_ss = str(now_hour) + ":" + str(now_minute) + \
        ":" + str(now_second)
    now_hh_mm_ss = datetime.datetime.strptime(str_hh_mm_ss, '%H:%M:%S')

    strSys_time_from = "00:00:00"
    strSys_time_to = "05:00:00"

    sys_time_from = datetime.datetime.strptime(strSys_time_from, '%H:%M:%S')
    sys_time_to = datetime.datetime.strptime(strSys_time_to, '%H:%M:%S')

    if now_hh_mm_ss >= sys_time_from and now_hh_mm_ss < sys_time_to:
        yesterday = nowDate - timedelta(1)
        yyyy_mm_dd = yesterday.strftime('%Y-%m-%d')
        str_hh = str(int(str(now_hour)) + 24)
        hh_mm_ss = str_hh + ":" + str(now_minute) + ":" + str(now_second)

    else:
        yyyy_mm_dd = nowDate.strftime('%Y-%m-%d')
        hh_mm_ss = nowDate.strftime('%H:%M:%S')

    if request.method == 'POST':
        if request.form.get("clockin_div", None) == "start":
            isStart = sql_select(user_id, "start", yyyy_mm_dd, cur)
            isFinish = sql_select(user_id, "finish", yyyy_mm_dd, cur)

            if not isStart[0] and not isFinish[0]:
                strSerno = "1"
                sql_insert(user_id, "start", yyyy_mm_dd,
                           strSerno, hh_mm_ss, cur)
                db.commit()
            else:
                if isStart[0] is not None == "1" and not isFinish[0]:
                    error_message = '終了ボタンが押下されていません'
                else:
                    error_message = '本日は開始ボタンを押すことはできません'

        elif request.form.get("clockin_div", None) == "finish":
            isStart = sql_select(user_id, "start", yyyy_mm_dd, cur)
            if isStart[0] is not None:
                isStop = sql_select(user_id, "stop", yyyy_mm_dd, cur)
                isResume = sql_select(user_id, "resume", yyyy_mm_dd, cur)

                if not isStop[0] and not isResume[0]:
                    strSerno = isStart[0]
                    sql_insert(user_id, "finish", yyyy_mm_dd,
                               strSerno, hh_mm_ss, cur)
                    db.commit()
                else:
                    if isStop[0] == isResume[0]:
                        strSerno = isStart[0]
                        sql_insert(user_id, "finish", yyyy_mm_dd,
                                   strSerno, hh_mm_ss, cur)
                        db.commit()
                    else:
                        error_message = '中断ボタンと再開ボタンの打刻数があっていません'
            else:
                error_message = '開始ボタンが押下されていません'

        elif request.form.get("clockin_div", None) == "stop":
            isStart = sql_select(user_id, "start", yyyy_mm_dd, cur)
            if isStart[0] is not None:
                isFinish = sql_select(user_id, "finish", yyyy_mm_dd, cur)
                isStop = sql_select(user_id, "stop", yyyy_mm_dd, cur)

                if isStop[0] is not None:
                    strSerno = str(int(isStop[0]) + 1)
                else:
                    strSerno = "1"

                if not isFinish[0]:
                    sql_insert(user_id, "stop", yyyy_mm_dd,
                               strSerno, hh_mm_ss, cur)
                    db.commit()
                else:
                    if int(isStart[0]) - int(isFinish[0]) == 1:
                        sql_insert(user_id, "stop", yyyy_mm_dd,
                                   strSerno, hh_mm_ss, cur)
                        db.commit()
                    else:
                        error_message = '開始ボタンが押下されていません'
            else:
                error_message = '開始ボタンが押下されていません'

        elif request.form.get("clockin_div", None) == "resume":
            isStart = sql_select(user_id, "start", yyyy_mm_dd, cur)
            if isStart[0] is not None:
                isStop = sql_select(user_id, "stop", yyyy_mm_dd, cur)
                isResume = sql_select(user_id, "resume", yyyy_mm_dd, cur)

                if isResume[0] is not None:
                    strSerno = str(int(isResume[0]) + 1)
                else:
                    strSerno = "1"

                if isStop[0] is not None and not isResume[0]:
                    sql_insert(user_id, "resume", yyyy_mm_dd,
                               strSerno, hh_mm_ss, cur)
                    db.commit()
                elif isStop[0] is not None and isResume[0] is not None:
                    if int(isStop[0]) - int(isResume[0]) == 1:
                        sql_insert(user_id, "resume", yyyy_mm_dd,
                                   strSerno, hh_mm_ss, cur)
                        db.commit()
                    else:
                        error_message = '中断と再開の打刻数がマッチしていません'

                else:
                    error_message = '中断ボタンが押下されていません'
            else:
                error_message = '開始ボタンが押下されていません'
    cur.execute(
        "select * from CLOCKIN_INFO where user_id = '{}'\
            and clockin_date = '{}' \
            and clockin_time=(select max(clockin_time) from CLOCKIN_INFO \
                                where user_id = '{}' and clockin_date = '{}')"
        .format(user_id, yyyy_mm_dd, user_id, yyyy_mm_dd)
    )
    latestClockInDiv = cur.fetchone()
    cur.close()
    logging.warning("#########latestClockInDivの取得結果#########")
    logging.warning(latestClockInDiv)
    logging.warning("#########yyyy_mm_dd#########")
    logging.warning(yyyy_mm_dd)
    user_name = session.get("user_name")
    return render_template('home/index.html', error_message=error_message,
                           user_name=user_name,
                           latestClockInDiv=latestClockInDiv)
