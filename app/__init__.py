import time

from flask import Flask, g
from flask_migrate import Migrate

from app.logging_manager import register_logging, register_sentry_sdk, log_database_and_response_time
from app.model.base import db
from app.exception import AuthFailed
from app.token_manager import register_blacklist_loader, jwt, register_jwt_error
from app.email_manager import mail

migrate = Migrate(compare_type=True, compare_server_default=True)


def create_upload_file(app_):
    import os
    base_path = app_.config['UPLOAD_FOLDER']
    if not os.path.exists(base_path):
        os.mkdir(base_path)

    # 创建存取标签图片的文件夹 TODO:写入配置
    tag_upload_files = os.path.join(base_path, 'tags')
    if not os.path.exists(tag_upload_files):
        os.mkdir(tag_upload_files)

    # 创建存取文章图片的文件夹 TODO:写入配置
    avatar_upload_files = os.path.join(base_path, 'posts')
    if not os.path.exists(avatar_upload_files):
        os.mkdir(avatar_upload_files)


def apply_cors(app_, config_name):
    from flask_cors import CORS
    if config_name != 'production':
        CORS(app_)


def register_blueprint(app_):
    from app.api.view.blueprint import api as api_blueprint
    app_.register_blueprint(api_blueprint)

    from app.api.admin.blueprint import admin as admin_blueprint
    app_.register_blueprint(admin_blueprint)

    # from app.web.blueprint import main as main_blueprint
    # app_.register_blueprint(main_blueprint)


def register_logstash():
    pass


def register_before_request(app_):
    @app_.before_request
    def before_request():
        # 记录 响应开始时间
        g.start_time = time.time()


def register_after_request(app_):
    @app_.after_request
    def after_all_request(response):
        log_database_and_response_time()
        return response


def create_app(config_name):
    from app.config import config
    app = Flask(__name__)
    app.config.from_object(config[config_name]())

    register_logging()

    create_upload_file(app)
    apply_cors(app, config_name)
    register_blueprint(app)
    register_before_request(app)
    register_after_request(app)
    register_sentry_sdk()
    register_blacklist_loader()
    register_jwt_error()

    jwt.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)

    return app


app = create_app('default')


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, create=db.create_all, drop=db.drop_all)


if __name__ == '__main__':
    app.run()
