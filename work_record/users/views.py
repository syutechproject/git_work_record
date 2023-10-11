from flask import Blueprint
from flask import redirect
from flask import request
from flask import render_template
from flask import session
from flask_bcrypt import Bcrypt
from flask_login import login_user
from flask_login import login_required


from work_record.models import get_db
from work_record.models import User

users = Blueprint('users', __name__, url_prefix='/work_record/users')


@users.route('/login', methods=['GET', 'POST'])
def login():
    error_message = ''
    user_id = ''

    if request.method == 'POST':
        user_id = request.form.get('user_id')
        password = request.form.get('password')

        db = get_db()
        curs = db.cursor()
        bcrypt = Bcrypt()
        curs.execute(
            "SELECT * FROM USERS WHERE user_id = '{user_id}'".format(
                user_id=user_id)
        )
        person = curs.fetchone()
        curs.close()
        if person:
            db_password = person[1].encode()
            if bcrypt.check_password_hash(db_password, password):
                user = User(user_id)
                login_user(user)
                session.permanent = True
                session["user_id"] = user_id
                session["user_name"] = person[2]
                return redirect('/work_record/home/')
        error_message = '入力されたユーザーIDもしくはパスワードが誤っています'

    return render_template('users/login.html', error_message=error_message,
                           user_id=user_id)


@users.route("/logout", methods=["GET"])
@login_required
def logout():
    session.pop('user_id', None)
    session.clear()
    return redirect("/work_record/users/login")
