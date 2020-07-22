import logging
import time
from functools import wraps
from logging.config import dictConfig

from flask import current_app, g, has_request_context, request
from flask_sqlalchemy import get_debug_queries

from app.myType import FlaskInstance, Response
import os


class RequestFormatter(logging.Formatter):
    def format(self, record):
        if has_request_context():
            record.url = request.url
            record.remote_addr = request.remote_addr
            record.ua = request.headers.get('User-Agent')
        else:
            record.url = None
            record.remote_addr = None

        return super().format(record)


# 展示定义
def logged(level: str = 'info', message: str = 'request log'):
    def decorate(fun):
        @wraps(fun)
        def wrapper(*args, **kwargs):
            logger = current_app.logger
            if level == 'warning':
                logger.warning(message)
            else:
                logger.info(f'{fun.__name__} : {message}')
            return fun(*args, **kwargs)

        return wrapper

    return decorate


def set_log_file(config: dict, app: FlaskInstance):
    from app.utils import create_dir
    dir_path = os.path.join(app.config['LOG_DIR'], app.name)
    create_dir(dir_path)
    handlers = config['handlers']
    handlers['file']['filename'] = os.path.join(dir_path, 'info.log')
    handlers['error']['filename'] = os.path.join(dir_path, 'error.log')


def register_logging(app: FlaskInstance, default_level=logging.INFO):
    import yaml
    # path = os.path.dirname(os.path.realpath(__file__))
    path = os.path.join(os.getcwd(), 'config/log.yaml')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            config = yaml.load(f, Loader=yaml.SafeLoader)
            set_log_file(config, app)
            logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)


def register_log_query_and_response_time(app: FlaskInstance):
    @app.before_request
    def before_request():
        # 记录 响应开始时间
        g.start_time = time.time()

    @app.after_request
    def after_all_request(response: Response):
        log_database_and_response_time()
        return response


def register_log_rollback(app: FlaskInstance):
    # 日志回滚
    time_file_handler = logging.handlers.TimedRotatingFileHandler(
        app.config['LOG_DIR']
    )


def register_sentry_sdk(app: FlaskInstance):
    from sentry_sdk.integrations.flask import FlaskIntegration
    import sentry_sdk
    sentry_sdk.init(
        dsn=app.config['SENTRY_DSN'],
        integrations=[FlaskIntegration()]
    )


def log_database_and_response_time():
    query_list = []
    for query in get_debug_queries():
        if query.duration >= current_app.config['SLOW_DB_QUERY_TIME']:
            query_list.append(query)
    response_time = time.time() - g.start_time
    current_app.logger.info(f'response time')
    if not query_list:
        current_app.logger.info(f'response time:{response_time}')
    else:
        query_list = [{
            'Slow query': query.statement,
            'Parameters:': query.parameters,
            'Duration': query.duration,
            'Context': query.context
        } for query in query_list]
        current_app.logger.warning(
            'response_time: %s\n query: %s'
            % (response_time, query_list)
        )
