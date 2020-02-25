import time

from flask import Flask, current_app, g
from flask_mail import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import get_debug_queries

from app.logging_ import register_logging
from app.model.base import db

migrate = Migrate(compare_type=True, compare_server_default=True)
mail = Mail()


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


def register_sentry_sdk():
    """
        错误处理集成
        参见:https://sentry.io/for/flask/
    :return:
    """
    from sentry_sdk.integrations.flask import FlaskIntegration
    import sentry_sdk
    import os
    sentry_sdk.init(
        dsn=os.getenv('SENTRY_DSN'),
        integrations=[FlaskIntegration()]
    )


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
        # 记录时间长的sql查询详情
        query_list = []
        for query in get_debug_queries():
            if query.duration >= current_app.config['SLOW_DB_QUERY_TIME']:
                query_list.append(query)
        # 计算响应时间
        diff = time.time() - g.start_time
        if not query_list:
            current_app.logger.info(f'response time:{diff}')
        else:
            query_list = [{
                'Slow query': query.statement,
                'Parameters:': query.parameters,
                'Duration': query.duration,
                'Context': query.context
            } for query in query_list]
            current_app.logger.warning(
                'response_time: %s\n query: %s'
                % (diff, query_list)
            )
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
