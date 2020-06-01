import os

from dotenv import load_dotenv
from werkzeug import run_simple
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from flask import request
from app.app_admin import create_admin_app
from app.app_frontend import create_view_app

APP_ROOT = os.path.join(os.path.dirname(__file__), '..')
dotenv_path = os.path.join(APP_ROOT, '.env')
load_dotenv(dotenv_path=dotenv_path)

app = create_view_app()

adminApp = create_admin_app()
app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    '/admin': adminApp
})


# app = DispatcherMiddleware(frontendApp, {
#     '/admin': adminApp
# })

@app.route('/logo.png')
@app.route('/robots.txt')
def frontend_static():
    return app.send_static_file(request.path[1:])


@app.route('/', defaults={'path': ''})
@app.route('/<path>')
@app.route('/article/<path>')
def frontend_view(path):
    return app.send_static_file('index.html')


# 写成<path:path> 似乎catch all 会失效
@adminApp.route('/', defaults={'path': ''})
@adminApp.route('/<path>')
@adminApp.route('/post/<path>')
def admin_view(path):
    return adminApp.send_static_file('index.html')


if __name__ == '__main__':
    run_simple(
        hostname='localhost',
        port=5000,
        application=app,
        use_reloader=True,
        use_debugger=True,
        use_evalex=True
    )
