import logging
from functools import wraps
from logging.config import dictConfig

from flask import has_request_context, request, current_app


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
    path = os.path.join(path, 'log.yaml')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            config = yaml.load(f, Loader=yaml.SafeLoader)
            logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)


def register_log_rollback(app):
    # 日志回滚
    time_file_handler = logging.handlers.TimedRotatingFileHandler(
        app.config['LOG_DIR']
    )
