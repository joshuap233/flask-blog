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


class BaseConfig(object):
    SQLALCHEMY_POOL_TIMEOUT = 1000
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # 分页功能,默认每页大小(如果前端没有传入)
    PAGESIZE = 10
    # 允许上传文件类型
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'svg', 'gif'}
    # 文件最大大小
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    # 数据库最慢查询时间,超过该时间则记录日志
    SLOW_DB_QUERY_TIME = 0.5
    SERVER_NAME = '127.0.0.1:5000'
    SECRET_KEY = '' or os.urandom(64)
    UPLOAD_FOLDER = os.path.join(os.getenv('HOME'), 'files')
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
    # app_admin存放日志文件夹名称
    LOG_DIR = os.path.join(os.getenv('HOME'), 'dev-logs')

    SQLALCHEMY_ENGINE_OPTIONS = {'pool_size': 100, 'pool_recycle': 280, 'pool_pre_ping': True}


class ProductionConfig(BaseConfig):
    MAIL_DEBUG = False
    SERVER_NAME = os.getenv('SERVER_NAME')

    # 数据库配置
    SQLALCHEMY_DATABASE_URI = f'mysql+mysqldb://root:{os.getenv("MYSQL_ROOT_PASSWORD")}@{os.getenv("MYSQL_ADDRESS")}/' \
                              f'blog?charset=utf8mb4'

    # 上传图片文件夹
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER')
    SECRET_KEY = os.getenv('SECRET_KEY')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    LOG_DIR = os.getenv('LOG_DIR')


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    # SQLALCHEMY_ECHO = True
    # SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = f'mysql+mysqldb://root:{os.getenv("MYSQL_ROOT_PASSWORD")}@{os.getenv("MYSQL_ADDRESS")}' \
                              f'/{os.getenv("DB_NAME")}?charset=utf8mb4'


class TestingConfig(BaseConfig):
    # 如果MAIL_SUPPRESS_SEND 为True,则单元测试时不会真正发送邮件
    # MAIL_SUPPRESS_SEND = False
    TESTING = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = f'mysql+mysqldb://root:root@127.0.0.1:3306/test_blog?charset=utf8mb4'
    UPLOAD_FOLDER = os.path.join(os.getenv('HOME'), 'test', 'files')
    LOG_DIR = os.path.join(os.getenv('HOME'), 'test', 'logs')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
}
