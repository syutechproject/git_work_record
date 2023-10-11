import os
import psycopg2
from datetime import timedelta
from flask import g
from flask import redirect
from flask_login import UserMixin
from flask import Flask
from flask_login import LoginManager


app = Flask(__name__)

# app.secret_key = os.urandom(24)
app.secret_key = "secret user"
app.permanent_session_lifetime = timedelta(minutes=15)

login_manager = LoginManager()
login_manager.init_app(app)


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        uri = os.environ.get('DATABASE_URL')
        if uri:
            if uri.startswith('postgres://'):
                uri = uri.replace('postgres://', 'postgresql://', 1)
                db = g._database = psycopg2.connect(uri)
                return db
        else:
            connector = psycopg2.connect(
                'postgresql://{user}:{password}@{host}:{port}/{dbname}'.format(
                 user="postgres",        # ユーザ
                 password="Andyxx5796",  # パスワード
                 host="localhost",       # ホスト名
                 port="5432",            # ポート
                 dbname="work_record")     # データベース名
                )
            return connector


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


class User(UserMixin):
    def __init__(self, userid):
        self.id = userid


@login_manager.user_loader
def load_user(userid):
    return User(userid)


@login_manager.unauthorized_handler
def unauthorized():
    return redirect('/work_record/users/login')
