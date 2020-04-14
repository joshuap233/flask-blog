from werkzeug.middleware.dispatcher import DispatcherMiddleware
from app.app_admin import app as adminApp
from app.app_frontend import app as viewApp
from werkzeug import run_simple

app = DispatcherMiddleware(viewApp, {
    '/blog/admin': adminApp
})

if __name__ == '__main__':
    run_simple(
        'localhost', 5000, app,
        use_reloader=True, use_debugger=True, use_evalex=True
    )
