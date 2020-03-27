class Config(object):
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # 邮件服务器
    MAIL_SERVER = 'smtp.exmail.qq.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USE_TSL = False
    MAIL_DEBUG = True
    # 分页功能,默认每页大小(如果前端没有传入)
    PAGESIZE = 10
    # 允许上传文件类型
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'svg', 'gif'}
    # 文件最大大小
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    # 数据库最慢查询时间,超过该时间则记录日志
    SLOW_DB_QUERY_TIME = 0.5
    # 存放日志文件夹名称


class ProductionConfig(Config):
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


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
