from flask import Flask
from flask_migrate import Migrate
from app.logging_manager import register_sentry_sdk
from app.model.baseDB import db
from app.myFlask import Flask
from app.myType import FlaskInstance, Callable
from app.utils import create_dir

migrate = Migrate(compare_type=True, compare_server_default=True)


def create_upload_folder(app: FlaskInstance):
    create_dir(app.config['UPLOAD_FOLDER'])


def apply_cors(app: FlaskInstance):
    from flask_cors import CORS
    CORS(app)


def init_db(app: FlaskInstance):
    db.init_app(app)
    with app.app_context():
        db.create_all()


# def register_app_shell(app: FlaskInstance):
#     @app.shell_context_processor
#     def make_shell_context():
#         return dict(db=db, create=db.create_all, drop=db.drop_all)


def create_app(register_config: Callable[[FlaskInstance], None], *args, **kwargs) -> FlaskInstance:
    app = Flask(*args, **kwargs)
    config_name = app.env
    # 注册config函数放在最前面(后面的配置会用到app.config)
    from app.config.config import config as common_config
    app.config.from_object(common_config[config_name]())

    register_config(app)
    if config_name == 'production':
        register_sentry_sdk(app)
    else:
        apply_cors(app)
    create_upload_folder(app)
    # register_app_shell(app)

    migrate.init_app(app, db)
    init_db(app)
    return app
