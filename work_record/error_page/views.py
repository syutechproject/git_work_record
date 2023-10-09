from flask import Blueprint
from flask import render_template


error_page = Blueprint('error_page', __name__,
                       url_prefix='/work_record/error_page')


@error_page.app_errorhandler(404)
def page_not_found(error):
    return render_template('error_page/not_found.html'), 404
