from app.exception import NotFound
from .blueprint import admin


@admin.errorhandler(404)
def page_not_found():
    raise NotFound('page not found')
