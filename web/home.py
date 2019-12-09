from flask import render_template

from .blueprint import main


@main.route('/', defaults={'path': ''})
@main.route('/<path:path>')
def main(path):
    return render_template('build/index.html')

