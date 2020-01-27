import pymysql
from flask import Flask
from flask_cors import CORS
from flask_mail import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from app.config import config

pymysql.install_as_MySQLdb()

db = SQLAlchemy()
migrate = Migrate()
mail = Mail()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name]())
    CORS(app)
    db.init_app(app)
    from app.api.view.blueprint import api as api_blueprint
    app.register_blueprint(api_blueprint)

    from app.api.admin.blueprint import admin as admin_blueprint
    app.register_blueprint(admin_blueprint)

    from app.web.blueprint import main as main_blueprint
    app.register_blueprint(main_blueprint)
    migrate.init_app(app, db)

    mail.init_app(app)
    return app


app = create_app('default')

if __name__ == '__main__':
    app.run()
