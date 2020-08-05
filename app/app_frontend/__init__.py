from app.api_limiter import limiter
from app.create_app import create_app
from app.logging_manager import register_logging, register_log_query_and_response_time
from app.myType import FlaskInstance


def register_blueprint(app: FlaskInstance):
    from app.app_frontend.api.blueprint import api as api_blueprint
    app.register_blueprint(api_blueprint)


def register_config(app: FlaskInstance):
    register_blueprint(app)
    limiter.init_app(app)
    # TODO 日志配置
    if app.env == 'production':
        register_logging(app)
        register_log_query_and_response_time(app)


def create_view_app(env=None):
    app = create_app(
        register_config,
        __name__,
        static_folder='static/',
        static_url_path='',
        env=env
    )
    return app
