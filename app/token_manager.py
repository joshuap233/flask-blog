from flask_jwt_extended import (
    decode_token, JWTManager, get_raw_jwt, verify_jwt_refresh_token_in_request,
    create_refresh_token, get_jwt_identity)
from app.exception import EmailValidateException, AuthFailed
from functools import wraps
from flask import current_app
from datetime import datetime

jwt = JWTManager()

blacklist = set()


def confirm_email_token(token):
    try:
        res = decode_token(token)
    except Exception as e:
        raise EmailValidateException(e.args)
    return res


def register_blacklist_loader():
    @jwt.token_in_blacklist_loader
    def check_if_token_in_blacklist(decrypted_token):
        jti = decrypted_token['jti']
        return jti in blacklist


def add_token_to_blacklist(token=None):
    if not token:
        jti = get_raw_jwt()['jti']
    else:
        try:
            res = decode_token(token)
            jti = res.get('jti')
        except Exception as e:
            raise AuthFailed(e.args)
    blacklist.add(jti)


def register_jwt_error():
    pass
    # @jwt.revoked_token_loader
    # def my_expired_token_callback():
    #     return {'status': 'failed'}, 401


def login_required(func):
    @wraps(func)
    def decorate(*args, **kwargs):
        """
            verify_jwt_refresh_token_in_request()
            needs to be run before get_raw_jwt in order for
            the token to be parsed and saved for this request
        """
        try:
            verify_jwt_refresh_token_in_request()
        except Exception as e:
            raise AuthFailed(e.args)
        identify = get_jwt_identity()
        expires_time = datetime.fromtimestamp(get_raw_jwt().get('exp'))
        remaining = expires_time - datetime.now()
        # 自动刷新token
        if remaining < current_app.config['JWT_MIN_REFRESH_SPACE']:
            create_refresh_token(identity=identify)
        return func(*args, **kwargs)

    return decorate
