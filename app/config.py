import os
from datetime import timedelta


class Config(object):
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DOMAIN = 'http://localhost:5000'
    SQLALCHEMY_DATABASE_URI = 'mysql+cymysql://root:root@localhost:3306/dev_blog?charset=utf8mb4'
    SECRET_KEY = os.getenv('SECRET_KEY') or os.urandom(64)
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USE_TSL = False
    MAIL_DEBUG = True
    SERVER_NAME = None
    PAGESIZE = 10
    UPLOAD_FOLDER = os.path.join(os.getenv('HOME'), 'test')
    ALLOWED_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.svg', '.gif'}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    SLOW_DB_QUERY_TIME = 0.5
    # 存放日志文件夹名称
    LOG_DIR = 'log'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=1)
    JWT_SECRET_KEY = os.urandom(32)
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
    # token离过期1小时自动刷新
    JWT_MIN_REFRESH_SPACE = timedelta(hours=1)
    VERIFICATION_CODE_LENGTH = 6
    # 验证码过期时间
    VERIFICATION_CODE_EXPIRE = timedelta(minutes=5)


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'picture')
    SECRET_KEY = os.getenv('SECRET_KEY')
    MAIL_DEBUG = False


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class TestingConfig(Config):
    # 如果MAIL_SUPPRESS_SEND 为True,则单元测试时不会真正发送邮件
    # MAIL_SUPPRESS_SEND = False
    TESTING = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = 'mysql+cymysql://root:root@localhost:3306/test_blog?charset=utf8mb4'


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
