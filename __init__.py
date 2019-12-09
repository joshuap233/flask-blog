import pymysql
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .config import config

pymysql.install_as_MySQLdb()

db = SQLAlchemy()
migrate = Migrate()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name]())
    CORS(app)
    db.init_app(app)
    from .api.blueprint import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')
    # with app.app_context():
    #     db.create_all()
    from .web.blueprint import main as main_blueprint
    app.register_blueprint(main_blueprint)
    migrate.init_app(app, db)
    return app
