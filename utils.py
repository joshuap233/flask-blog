from functools import wraps

from flask import request, jsonify

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
