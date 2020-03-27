from flask_migrate import Migrate

from app.email_manager import mail
from app.exception import AuthFailed
from app.logging_manager import register_logging, register_sentry_sdk, register_log_query_and_response_time
from app.model.baseDb import db
from app.token_manager import register_blacklist_loader, jwt, register_jwt_error
from .myFlask import Flask

migrate = Migrate(compare_type=True, compare_server_default=True)


def create_upload_file(app):
    import os
    base_path = app.config['UPLOAD_FOLDER']
    if not os.path.exists(base_path):
        os.mkdir(base_path)


def apply_cors(app, config_name):
    from flask_cors import CORS
    if config_name != 'production':
        CORS(app)


def register_blueprint(app):
    from app.api.view.blueprint import api as api_blueprint
    app.register_blueprint(api_blueprint)

    from app.api.admin.blueprint import admin as admin_blueprint
    app.register_blueprint(admin_blueprint)

    from app.web.blueprint import main as main_blueprint
    app.register_blueprint(main_blueprint)


def register_logstash():
    pass


def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()


def create_app(config_name):
    from app.config.config import config as common_config
    from app.config.security import config as security_config
    app = Flask(__name__, template_folder='static/', static_folder='static/build/')
    app.config.from_object(common_config[config_name]())
    app.config.from_object(security_config[config_name]())
    if config_name == 'production':
        register_logging()
        register_log_query_and_response_time(app)
    register_sentry_sdk(app)
    create_upload_file(app)
    apply_cors(app, config_name)
    register_blueprint(app)
    register_blacklist_loader()
    register_jwt_error()

    jwt.init_app(app)

    init_db(app)

    migrate.init_app(app, db)
    mail.init_app(app)

    return app


app = create_app('default')


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, create=db.create_all, drop=db.drop_all)


if __name__ == '__main__':
    app.run()
