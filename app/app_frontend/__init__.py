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


def create_view_app(env=None):
    app = create_app(
        register_config,
        __name__,
        static_folder='static/',
        static_url_path='',
        env=None
    )
    return app
