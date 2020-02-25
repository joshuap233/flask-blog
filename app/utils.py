import time
from functools import wraps

from flask import request, jsonify, current_app
from flask_mail import Message

from app import mail
from app.exception import AuthFailed, ParameterException
from app.model.db import User


def time2stamp(time_, format_='%Y/%m/%d %H:%M'):
    from wtforms.validators import StopValidation
    try:
        return int(time.mktime(time.strptime(time_, format_)))
    except:
        # 停止验证
        raise StopValidation(message="日期格错误")


def format_time(timestamp, format_='%Y/%m/%d %H:%M'):
    return time.strftime(format_, time.localtime(timestamp))


def generate_res(status='success', **kwargs):
    from app.model.view_model import BaseView
    for key, value in kwargs.items():
        if isinstance(value, BaseView):
            kwargs[key] = value.__dict__
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
            raise AuthFailed()
        user = User.query.get_or_404(int(uid))
        if not user.is_active or not user.confirm_token(token):
            # 验证token失败直接将is_active设置为false
            user.update(is_active=False)
            raise AuthFailed()
        return func(*args, **kwargs)

    return check_login


def get_attr(keys: list, data: dict):
    return [data.get(key) for key in keys]


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(to, subject, content):
    from threading import Thread
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


def send_register_email():
    pass


def filters_filename(filename):
    from uuid import uuid1
    from werkzeug.utils import secure_filename
    from os import path
    filename = secure_filename(filename)
    ext_name = path.splitext(filename)[-1]
    if ext_name not in current_app.config['ALLOWED_EXTENSIONS']:
        raise ParameterException('扩展名错误')
    return str(uuid1()) + ext_name
