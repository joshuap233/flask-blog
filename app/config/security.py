import os
from datetime import timedelta


class SecurityConfig(object):
    SERVER_NAME = '127.0.0.1:5000'
    SECRET_KEY = '' or os.urandom(64)
    MAIL_USERNAME = ''
    MAIL_PASSWORD = ''
    UPLOAD_FOLDER = 'files'
    # 存放日志文件夹名称
    LOG_DIR = 'log'
    # token过期时间
    JWT_REFRESH_TOKEN_EXPIRES = '' or timedelta(days=1)
    JWT_SECRET_KEY = '' or os.urandom(64)
    # token黑名单
    JWT_BLACKLIST_ENABLED = True
    # 这个字段不需要配置
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
    # token离过期1小时自动刷新
    JWT_MIN_REFRESH_SPACE = '' or timedelta(hours=1)
    # 验证码长度
    VERIFICATION_CODE_LENGTH = '' or 6
    # 验证码过期时间
    VERIFICATION_CODE_EXPIRE = '' or timedelta(minutes=5)
    # 错误处理集成     参见:https://sentry.io/for/flask/
    SENTRY_DSN = ''


class ProductionConfig(SecurityConfig):
    # 数据库配置
    SQLALCHEMY_DATABASE_URI = 'mysql+cymysql://root:root@localhost:3306/dev_blog?charset=utf8mb4'
    # 上传图片文件夹
    UPLOAD_FOLDER = 'files'
    SECRET_KEY = '' or os.urandom(64)


class DevelopmentConfig(SecurityConfig):
    SQLALCHEMY_DATABASE_URI = 'mysql+cymysql://root:root@localhost:3306/dev_blog?charset=utf8mb4'


class TestingConfig(SecurityConfig):
    SQLALCHEMY_DATABASE_URI = 'mysql+cymysql://root:root@localhost:3306/test_blog?charset=utf8mb4'


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
