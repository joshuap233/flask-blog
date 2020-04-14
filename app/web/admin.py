from flask import Blueprint

admin_page = Blueprint(
    'admin_page',
    __name__,
    static_folder='../static/admin/',
)


@admin_page.route('/admin', defaults={'path': ''})
@admin_page.route('/admin/<path:path>')
def admin_view(path):
    return admin_page.send_static_file('index.html')
