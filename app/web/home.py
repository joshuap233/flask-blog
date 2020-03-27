from flask import render_template

from .blueprint import main


# @main.route('/', defaults={'path': ''})
# @main.route('/<path:path>')
# def home(path):
#     return render_template('build/index.html')
#

@main.route('/admin', defaults={'path': ''})
@main.route('/admin/<path:path>')
def admin(path):
    return render_template('build/index.html')
