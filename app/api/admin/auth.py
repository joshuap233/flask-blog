from flask import request

from app.model.db import User
from app.model.view_model import UserInfoView, LoginView
from app.utils import generate_res
from app.validate.validate import (
    RegisterValidate, UserValidate, LoginValidate, EmailCodeValidate,
    EmailValidate, RecoveryPasswordValidate, ResetPasswordValidate)
from .blueprint import admin
from flask_jwt_extended import get_jwt_identity
from app.email_manager import (
    send_recovery_pass_email, send_change_email_email, send_validate_new_email_email, send_change_pass_warn)
from app.token_manager import add_token_to_blacklist, login_required


@admin.route('/sessions', methods=['POST'])
def login_view():
    form = LoginValidate().validate_api()
    user = User.search_by(**form.login)
    user.check_password(form.password.data)
    return generate_res(data=LoginView(user))


@admin.route('/sessions', methods=['DELETE'])
@login_required
def logout_view():
    add_token_to_blacklist()
    return generate_res()


@admin.route('/sessions')
@login_required
def auth_view():
    return generate_res()


@admin.route('/user', methods=['POST'])
def register_view():
    form = RegisterValidate().validate_api()
    user = User.create(**form.data)
    if form.email.data:
        code = user.set_code()
        send_validate_new_email_email(user.email, code)
    return generate_res()


@admin.route('/user', methods=['PATCH', 'GET'])
@login_required
def user_info_view():
    uid = request.headers.get('identify')
    user = User.search_by(id=uid)
    if request.method == 'PATCH':
        form = UserValidate().validate_api()
        user.update(**form.data)
        return generate_res()
    return generate_res(data=UserInfoView(user))


@admin.route('/user/password/reset', methods=['POST'])
@login_required
def reset_password_view():
    form = ResetPasswordValidate().validate_api()
    user = User.reset_password(form)
    send_change_pass_warn(email=user.email)
    return generate_res()


# 忘记密码功能完成
# TODO : 忘记密码时,发送验证码
@admin.route('/user/password/recovery', methods=['GET', 'PUT'])
def recovery_password_view():
    if request.method == 'PUT':
        form = RecoveryPasswordValidate().validate_api()
        user = User.validate_code_by(form.code.data, email=form.email.data)
        user.update(password=form.password.data)
        send_change_pass_warn(email=user.email)
        return generate_res()
    form = EmailValidate().validate_api()
    user = User.search_by(email=form.email.data)
    user.validate_email_effect()
    code = user.set_code()
    send_recovery_pass_email(user.email, code)
    return generate_res()


@admin.route('/user/email/reset', methods=['POST', 'GET'])
@login_required
def reset_email_view():
    if request.method == 'POST':
        # 确认验证码,并发送验证码至新邮件地址
        form = EmailCodeValidate().validate_api()
        uid = get_jwt_identity()
        user = User.validate_code_by(form.code.data, id=uid)
        user.update(email=form.email.data)
        code = user.set_code()
        send_validate_new_email_email(user.email, code)
        return generate_res()
    # 发送验证码至旧邮件地址
    uid = get_jwt_identity()
    user = User.search_by(id=uid)
    # TODO: 邮件未验证的处理
    user.validate_email_effect()
    code = user.set_code()
    send_change_email_email(user.email, code)
    return generate_res()


@admin.route('/user/email', methods=['PUT'])
def validate_email_view():
    form = EmailCodeValidate().validate_api()
    user = User.search_by(email=form.email.data)
    user.update(email_is_validate=True)
    return generate_res()
