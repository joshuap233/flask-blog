from functools import wraps
from threading import Thread

from flask import request, jsonify, current_app
from flask_mail import Message

from . import mail
from .database import User


def generate_res(state, msg, **kwargs):
    status = {
        'status': state,
        'msg': msg
    }
    status.update(kwargs)
    return jsonify(status)


def required_login(func):
    @wraps(func)
    def check_login(*args, **kwargs):
        data = request.headers
        uid = data.get('identify')
        token = data.get('Authorization')
        user = User.query.filter_by(id=uid).first()
        if user and user.is_active and user.confirm_token(token):
            return func(*args, **kwargs)
        return generate_res('failed', 'check login')

    return check_login


def get_attr(keys: list, data: dict):
    return [data.get(key) for key in keys]


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(to, subject, content):
    app = current_app._get_current_object()
    msg = Message(
        subject=subject,
        sender=current_app.config['MAIL_USERNAME'],
        recipients=[to]
    )
    msg.body = content
    # msg.html = "<b>testing</b>"
    t = Thread(target=send_async_email, args=[app, msg])
    t.start()
