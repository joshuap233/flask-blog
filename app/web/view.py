from flask import Blueprint, current_app

view_page = Blueprint(
    'view_page',
    __name__,
)


@view_page.route('/', defaults={'path': ''})
@view_page.route('/<path:path>')
def home(path):
    return current_app.send_static_file('index.html')
