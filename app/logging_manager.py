import logging
from functools import wraps
from logging.config import dictConfig

from flask import has_request_context, request
from flask_sqlalchemy import get_debug_queries
import time

from flask import Flask, current_app, g


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
def logged(level='info', message='request log'):
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


def register_logging(default_level=logging.INFO):
    import os
    import yaml
    path = os.path.dirname(os.path.realpath(__file__))
    path = os.path.join(path, './config/log.yaml')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            config = yaml.load(f, Loader=yaml.SafeLoader)
            logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)


def register_log_query_and_response_time(app):
    @app.before_request
    def before_request():
        # 记录 响应开始时间
        g.start_time = time.time()

    @app.after_request
    def after_all_request(response):
        log_database_and_response_time()
        return response


def register_log_rollback(app):
    # 日志回滚
    time_file_handler = logging.handlers.TimedRotatingFileHandler(
        app.config['LOG_DIR']
    )


def register_sentry_sdk():
    from sentry_sdk.integrations.flask import FlaskIntegration
    import sentry_sdk
    import os
    sentry_sdk.init(
        dsn=os.getenv('SENTRY_DSN'),
        integrations=[FlaskIntegration()]
    )


def log_database_and_response_time():
    query_list = []
    for query in get_debug_queries():
        if query.duration >= current_app.config['SLOW_DB_QUERY_TIME']:
            query_list.append(query)
    response_time = time.time() - g.start_time
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
