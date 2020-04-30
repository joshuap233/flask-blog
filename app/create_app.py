from flask import Flask
from flask_migrate import Migrate

from app.logging_manager import register_sentry_sdk
from app.model.baseDB import db
from app.myFlask import Flask
from app.myType import FlaskInstance, Callable

migrate = Migrate(compare_type=True, compare_server_default=True)


def create_upload_file(app: FlaskInstance):
    import os
    base_path = app.config['UPLOAD_FOLDER']
    if not os.path.exists(base_path):
        os.mkdir(base_path)


def apply_cors(app: FlaskInstance):
    from flask_cors import CORS
    CORS(app)


def init_db(app: FlaskInstance):
    db.init_app(app)
    with app.app_context():
        db.create_all()


def register_app_shell(app: FlaskInstance):
    @app.shell_context_processor
    def make_shell_context():
        return dict(db=db, create=db.create_all, drop=db.drop_all)


def create_app(register_config: Callable[[FlaskInstance, str], None], *args, **kwargs) -> FlaskInstance:
    config = kwargs.pop('env', None)
    app = Flask(*args, **kwargs)
    config_name = config if config else app.env

    register_config(app, config_name)
    from app.config.config import config as common_config
    from app.config.security import config as security_config

    app.config.from_object(common_config[config_name]())
    app.config.from_object(security_config[config_name]())
    if config_name == 'production':
        register_sentry_sdk(app)
    else:
        apply_cors(app)
    create_upload_file(app)
    register_app_shell(app)

    migrate.init_app(app, db)
    init_db(app)
    return app
