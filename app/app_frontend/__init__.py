from werkzeug.serving import run_simple
from app.create_app import create_app
from app.logging_manager import register_logging, register_log_query_and_response_time


def register_blueprint(app):
    from app.app_frontend.api.blueprint import api as api_blueprint
    app.register_blueprint(api_blueprint)


def register_config(app, config_name):
    register_blueprint(app)
    # TODO 日志配置
    if config_name == 'production':
        register_logging()
        register_log_query_and_response_time(app)


app = create_app(
    register_config,
    __name__,
    static_folder='static/',
    static_url_path='/view/'
)


@app.route('/<path:path>')
@app.route('/', defaults={'path': ''})
def font_end_view(path):
    return app.send_static_file('index.html')


if __name__ == '__main__':
    run_simple(
        hostname='localhost',
        port=5000,
        application=app,
        use_reloader=True,
        use_debugger=True,
        use_evalex=True
    )
