from flask import Flask
from flask_cors import CORS
from flask_mail import Mail
from flask_migrate import Migrate

from app.config import config
from app.model.base import db

migrate = Migrate(compare_type=True, compare_server_default=True)
mail = Mail()


def register_blueprint(app_):
    from app.api.view.blueprint import api as api_blueprint
    app_.register_blueprint(api_blueprint)

    from app.api.admin.blueprint import admin as admin_blueprint
    app_.register_blueprint(admin_blueprint)

    from app.web.blueprint import main as main_blueprint
    app_.register_blueprint(main_blueprint)


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name]())
    if config_name != 'production':
        CORS(app)
    register_blueprint(app)
    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    return app


app = create_app('default')


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, create=db.create_all, drop=db.drop_all)


if __name__ == '__main__':
    app.run()
