from flask import render_template

from .blueprint import main


@main.route('/', defaults={'path': ''})
@main.route('/<path:path>')
def home(path):
    return render_template('build/index.html')


@main.route('/admin/')
def admin():
    return render_template('admin.html')
