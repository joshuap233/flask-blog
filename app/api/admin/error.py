from .blueprint import admin
from app.utils import generate_res


@admin.errorhandler(404)
def page_not_found():
    return generate_res('failed', "page not found"), 404
