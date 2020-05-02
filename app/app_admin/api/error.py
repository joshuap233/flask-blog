from flask import current_app
from werkzeug.exceptions import HTTPException

from app.exception import RequestEntityTooLarge
from .blueprint import admin


@admin.errorhandler(Exception)
def handle_error(e):
    if isinstance(e, HTTPException):
        pass
    current_app.logger.warning(e)
    res = e.get_response() if hasattr(e, 'get_response') else e.args
    return res


@admin.errorhandler(413)
def file_too_large(e):
    current_app.logger.warning(e)
    raise RequestEntityTooLarge("文件太大")
