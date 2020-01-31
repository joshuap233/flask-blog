from functools import wraps
from threading import Thread

from flask import request, jsonify, current_app
from flask_mail import Message

from app.model.db import User
from . import mail


def generate_res(status, **kwargs):
    status = {
        'status': status,
    }
    status.update(kwargs)
    return jsonify(status)


def login_required(func):
    @wraps(func)
    def check_login(*args, **kwargs):
        data = request.headers
        uid = data.get('identify')
        token = data.get('Authorization')
        if not uid or not token:
            return generate_res('failed', msg='check login'), 401
        user = User.query.get(int(uid))
        if not user:
            return generate_res('failed', msg='user not found'), 401
        if user.is_active and user.confirm_token(token) and user.is_validate:
            return func(*args, **kwargs)
        user.is_active = False
        user.auto_add()
        return generate_res('failed', msg='check login'), 401

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
