from .email_manager import mail
from .token_manager import register_blacklist_loader, jwt, register_jwt_error
from werkzeug.serving import run_simple
from app.create_app import create_app
from app.logging_manager import register_logging, register_log_query_and_response_time


def register_blueprint(app):
    from app.app_admin.api.blueprint import admin as admin_blueprint
    app.register_blueprint(admin_blueprint)


def register_config(app, config_name):
    register_blueprint(app)
    register_blacklist_loader()
    register_jwt_error()

    jwt.init_app(app)

    mail.init_app(app)
    # TODO 日志配置
    if config_name == 'production':
        register_logging()
        register_log_query_and_response_time(app)


def create_admin_app(env=None):
    app = create_app(
        register_config,
        __name__,
        static_folder='static/',
        static_url_path='',
        env=env
    )
    return app
