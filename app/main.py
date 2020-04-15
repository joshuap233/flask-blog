import os
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from app.app_admin import app as adminApp
from app.app_frontend import app
from werkzeug import run_simple
from dotenv import load_dotenv

APP_ROOT = os.path.join(os.path.dirname(__file__), '..')
dotenv_path = os.path.join(APP_ROOT, '.env')
load_dotenv(dotenv_path=dotenv_path)

app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    '/admin': adminApp
})

if __name__ == '__main__':
    run_simple(
        hostname='localhost',
        port=5000,
        application=app,
        use_reloader=True,
        use_debugger=True,
        use_evalex=True
    )
