from flask import current_app
from werkzeug.exceptions import HTTPException

from app.exception import RequestEntityTooLarge
from .blueprint import admin


@admin.errorhandler(HTTPException)
def handle_error(e):
    current_app.logger.warning(e)
    return e.get_response()


@admin.errorhandler(413)
def file_too_large(e):
    current_app.logger.warning(e)
    raise RequestEntityTooLarge("文件太大")
