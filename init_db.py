from flask_bcrypt import Bcrypt
from work_record.models import get_db
from work_record import app


userid = 'roger'
name = 'federer'

bcrypt = Bcrypt()
password = "1234xyA1"
hashed_password = bcrypt.generate_password_hash(password=password)
rev_hashed_password = hashed_password.decode()


# with app.app_context():
#     db = get_db()
#     db.execute("delete from USERS")
#     db.commit()
#     db.close()


with app.app_context():
    db = get_db()
    cur = db.cursor()
    cur.execute(
        "insert into USERS (user_id, password, name)\
            values('{user_id}', '{password}', '{name}')".format(
            user_id=userid,
            password=rev_hashed_password,
            name=name)
        )
    db.commit()
    db.close()

# with app.app_context():
#     db = get_db()
#     db.execute("delete from CLOCKIN_INFO where clockin_date = '2023-06-17'")
#     db.commit()
#     db.close()


# with app.app_context():
#     db = get_db()
#     cur = db.cursor()
#     cur.execute("CREATE TABLE USERS\
#                ( user_id text primary key not null,\
#                  password text not null,\
#                  name text not null );")
#     db.commit()
#     db.close()


with app.app_context():
    db = get_db()
    cur = db.cursor()
    cur.execute("CREATE TABLE CLOCKIN_INFO \
               (user_id text not null, clockin_date text not null,\
                clockin_div text not null, serno text not null, \
               clockin_time text not null, \
               primary key (user_id,clockin_date,clockin_div,serno), \
               FOREIGN KEY (user_id) REFERENCES USERS (user_id) );")
    db.commit()
    db.close()
