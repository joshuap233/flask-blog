from werkzeug.serving import run_simple
from app.shared.create_app import create_app
from app.logging_manager import register_logging, register_log_query_and_response_time


def register_blueprint(app):
    from .api.blueprint import api as api_blueprint
    app.register_blueprint(api_blueprint)


def register_config(app, config_name):
    register_blueprint(app)
    # TODO 日志配置
    if config_name == 'production':
        register_logging()
        register_log_query_and_response_time(app)
    return app


app = create_app(register_config)


@app.route('/blog/admin/', defaults={'path': ''})
@app.route('/blog/admin/<path:path>')
def admin_view(path):
    return app.send_static_file('admin/index.html')


if __name__ == '__main__':
    run_simple(
        'localhost', 5000, app,
        use_reloader=True, use_debugger=True, use_evalex=True
    )
