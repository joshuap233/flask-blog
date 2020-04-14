import os
from datetime import timedelta


class SecurityConfig(object):
    SERVER_NAME = '127.0.0.1:5000'
    SECRET_KEY = '' or os.urandom(64)
    MAIL_USERNAME = 'shu@shushugo.com'
    MAIL_PASSWORD = '7jGyraxhFtLDKK7z'
    UPLOAD_FOLDER = os.path.join(os.getenv('HOME'), 'files')
    # 存放日志文件夹名称
    LOG_DIR = 'log'
    # token过期时间
    JWT_REFRESH_TOKEN_EXPIRES = '' or timedelta(hours=1)
    JWT_SECRET_KEY = '' or os.urandom(64)
    # token黑名单
    JWT_BLACKLIST_ENABLED = True
    # 这个字段不需要配置
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
    # token离过期10分钟自动刷新
    JWT_MIN_REFRESH_SPACE = '' or timedelta(minutes=10)
    # 验证码过期时间
    VERIFICATION_CODE_EXPIRE = '' or timedelta(minutes=5)
    # 错误处理集成     参见:https://sentry.io/for/flask/
    SENTRY_DSN = 'https://4a5aa6f1bb9f45eaa1556d0022d04446@sentry.io/5177271'


class ProductionConfig(SecurityConfig):
    SERVER_NAME = '127.0.0.1'

    # 数据库配置
    SQLALCHEMY_DATABASE_URI = 'mysql+cymysql://root:root@172.17.0.1:3306/pro_blog?charset=utf8mb4'
    # 上传图片文件夹
    UPLOAD_FOLDER = '/files'
    SECRET_KEY = b'\x1b\x80\x9b\x8c5\x18\x99\xf2;q;\xaf\xaa\x1fg4\xf7\n\xd0?\xb6\x1a\x10\xee\x0f8\xd7\x97O\x01D7'
    JWT_SECRET_KEY = b'\x1b\x80\x9b\x8c5\x18\x99\xf2;q;\xaf\xaa\x1fg4\xf7\n\xd0?\xb6\x1a\x10\xee\x0f8\xd7\x97O\x01D7'


class DevelopmentConfig(SecurityConfig):
    SQLALCHEMY_DATABASE_URI = 'mysql+cymysql://root:root@127.0.0.1:3306/dev_blog?charset=utf8mb4'


class TestingConfig(SecurityConfig):
    SQLALCHEMY_DATABASE_URI = 'mysql+cymysql://root:root@127.0.0.1:3306/test_blog?charset=utf8mb4'


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}
