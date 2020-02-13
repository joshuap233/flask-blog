import os


class Config(object):
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    DOMAIN = 'http://localhost:5000'
    SQLALCHEMY_DATABASE_URI = 'mysql+cymysql://root:root@localhost:3306/dev_blog?charset=utf8mb4'
    UPLOAD_FOLDER = os.path.join(os.getenv('HOME'), 'test')
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


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER')
    SECRET_KEY = os.getenv('SECRET_KEY')
    MAIL_DEBUG = False


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = True


class TestingConfig(Config):
    TESTING = True
    # 如果MAIL_SUPPRESS_SEND 为True,则单元测试时不会真正发送邮件
    # MAIL_SUPPRESS_SEND = False
    SQLALCHEMY_DATABASE_URI = 'mysql+cymysql://root:root@localhost:3306/test_blog?charset=utf8mb4'


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
