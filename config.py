class Config(object):
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root:root@localhost:3306/blog?charset=utf8mb4'
    UPLOAD_FOLDER = '' or '/home/pjs/test'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = ''


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
