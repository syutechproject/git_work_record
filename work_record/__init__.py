from work_record.users.views import users
from work_record.error_page.views import error_page
from work_record.clockin_help.views import clockin_help
from work_record.clockin_check.views import clockin_check
from work_record.home.views import home
from work_record.models import app


app.register_blueprint(users)
app.register_blueprint(clockin_check)
app.register_blueprint(clockin_help)
app.register_blueprint(error_page)
app.register_blueprint(home)
