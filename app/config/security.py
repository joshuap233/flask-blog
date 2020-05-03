import os
from datetime import timedelta

# 如果设置该变量,则会在每个后台接口前添加相应的字符串
API_SECURITY_STRING = os.getenv("API_SECURITY_STRING")
MAIL_USERNAME = os.getenv("MAIL_USERNAME")
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
MAIL_SERVER = 'smtp.exmail.qq.com'
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_USE_TLS = False
MAIL_DEBUG = True


class SecurityConfig(object):
    SERVER_NAME = '127.0.0.1:5000'
    SECRET_KEY = '' or os.urandom(64)
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
    SENTRY_DSN = os.getenv('SENTRY_DSN')


class ProductionConfig(SecurityConfig):
    SERVER_NAME = os.getenv('SERVER_NAME')

    # 数据库配置
    SQLALCHEMY_DATABASE_URI = f'mysql+mysqldb://root:{os.getenv("MYSQL_ROOT_PASSWORD")}@{os.getenv("MYSQL_ADDRESS")}' \
                              f'/blog?charset=utf8mb4'

    # 上传图片文件夹
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER')
    SECRET_KEY = os.getenv('SECRET_KEY')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')


class DevelopmentConfig(SecurityConfig):
    SQLALCHEMY_DATABASE_URI = f'mysql+mysqldb://root:{os.getenv("MYSQL_ROOT_PASSWORD")}@{os.getenv("MYSQL_ADDRESS")}' \
                              f'/{os.getenv("DB_NAME")}?charset=utf8mb4'


class TestingConfig(SecurityConfig):
    SQLALCHEMY_DATABASE_URI = f'mysql+mysqldb://root:root@127.0.0.1:3306/test_blog?charset=utf8mb4'


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}
