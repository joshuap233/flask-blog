from flask import request

from ..email_manager import (
    send_register_success_email,
    send_recovery_pass_email, send_change_email_email, send_change_pass_warn,
    send_change_email_success_email
)
from app.exception import EmailNotFound, EmailHasAdd
from app.model.db import User
from app.app_admin.view_model import UserInfoView, LoginView
from ..token_manager import add_token_to_blacklist, login_required, login_check_without_refresh
from app.utils import generate_res
from ..validate.validate import (
    RegisterValidate, UserValidate, LoginValidate, EmailCodeValidate,
    EmailValidate, RecoveryPasswordValidate, ResetPasswordValidate)
from .blueprint import admin
from app.signals import cache_signals, SIGNAL_SENDER


@admin.route('/sessions', methods=['POST'], security=False)
def login_view():
    form = LoginValidate().validate_api()
    user = User.search_by(**form.login)
    user.check_password(form.password.data)
    return generate_res(data=LoginView(user))


@admin.route('/sessions', methods=['DELETE'])
@login_check_without_refresh
def logout_view():
    add_token_to_blacklist()
    return generate_res()


# 用于验证是否登录
@admin.route('/sessions', security=False)
@login_required
def auth_view():
    return generate_res()


# 检查是否注册
@admin.route('/user/register', security=False)
def check_register_view():
    User.check_register()
    return generate_res()


@admin.route('/user', methods=['POST'], security=False)
def register_view():
    User.check_register()
    form = RegisterValidate().validate_api()
    User.create(**form.data)
    if form.email.data:
        send_register_success_email(email=form.email.data)
    return generate_res()


@admin.route('/user', methods=['PATCH', 'GET'])
@login_required
def user_info_view():
    if request.method == 'PATCH':
        form = UserValidate().validate_api()
        user = User.get_user()
        user.update(**form.data)
        cache_signals.send(SIGNAL_SENDER['changeUserInfo'])
        return generate_res()
    user = User.get_user()
    return generate_res(data=UserInfoView(user))


@admin.route('/user/password/reset', methods=['PATCH'])
@login_required
def reset_password_view():
    form = ResetPasswordValidate().validate_api()
    user = User.reset_password(form)
    send_change_pass_warn(email=user.email)
    return generate_res()


# 找回密码
@admin.route('/user/password/recovery', methods=['GET', 'PUT'], security=False)
def recovery_password_view():
    if request.method == 'PUT':
        form = RecoveryPasswordValidate().validate_api()
        user = User.validate_code_by(form.code.data, email=form.email.data)
        user.update(password=form.password.data)
        send_change_pass_warn(email=user.email)
        return generate_res()
    # 查询参数传入email
    form = EmailValidate().validate_api()
    user = User.search_by(email=form.email.data)
    code = user.set_code()
    send_recovery_pass_email(user.email, code)
    return generate_res()


# 修改/添加邮箱
@admin.route('/user/email', methods=['PUT', 'GET', 'POST'])
@login_required
def email_view():
    if request.method == 'PUT':
        # 确认验证码, 修改邮件地址
        form = EmailCodeValidate().validate_api()
        user = User.get_user()
        user = User.validate_code_by(form.code.data, id=user.id)
        user.update(email=form.email.data)
        send_change_email_success_email(email=user.email)
        return generate_res()
    elif request.method == 'POST':
        # 添加邮件
        form = EmailValidate().validate_api()
        user = User.get_user()
        if user.email:
            raise EmailHasAdd()
        user.update(email=form.email.data)
        return generate_res()
    # 发送验证码至旧邮件地址,以修改邮件
    user = User.get_user()
    if not user.email:
        raise EmailNotFound()
    code = user.set_code()
    send_change_email_email(user.email, code)
    return generate_res()
