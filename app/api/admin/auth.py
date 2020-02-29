from flask import request

from app.model.db import User
from app.model.view_model import UserInfoView, LoginView
from app.utils import generate_res, get_attr
from app.validate.validate import (
    RegisterValidate, UserValidate, LoginValidate, ChangeEmailValidate,
    EmailValidate, ForgetPasswordValidate, ResetPasswordValidate)
from .blueprint import admin
from flask_jwt_extended import get_jwt_identity
from app.email_manager import (
    send_validate_email_email, send_change_password_warn, send_forget_password_email, send_change_email_email)
from app.token_manager import confirm_email_token, add_token_to_blacklist, login_required


@admin.route('/user/register', methods=['POST'])
def register_view():
    form = RegisterValidate().validate_api()
    user = User.create(form.data)
    if form.email.data:
        send_validate_email_email(user=user, form=form)
    return generate_res()


@admin.route('/user/login', methods=['POST'])
def login_view():
    form = LoginValidate().validate_api()
    user = User.search_by(form.login)
    user.check_password(form.password.data)
    return generate_res(data=LoginView(user))


@admin.route('/user/logout', methods=['DELETE'])
def logout_view():
    add_token_to_blacklist()
    return generate_res()


@admin.route('/user/auth')
@login_required
def auth_view():
    return generate_res()


@admin.route('/user/info', methods=['PUT', 'GET'])
@login_required
def user_info_view():
    uid = request.headers.get('identify')
    user = User.search_by_id(uid)
    if request.method == 'PUT':
        form = UserValidate().validate_api()
        user.update(form.data)
        return generate_res()
    return generate_res(data=UserInfoView(user))


@admin.route('/user/password/forget', methods=['POST', 'GET'])
def forget_password_view():
    if request.method == 'POST':
        form = ForgetPasswordValidate().validate_api()
        user = User.validate_code(form)
        user.update(password=form.password.data)
        return generate_res()
    form = EmailValidate().validate_api()
    code = User.set_code_by(form=form)
    send_forget_password_email(form=form, code=code)
    return generate_res()


@admin.route('/user/password/reset', methods=['POST'])
@login_required
def reset_password_view():
    form = ResetPasswordValidate().validate_api()
    user = User.reset_password(form)
    send_change_password_warn(user=user)
    return generate_res()


@admin.route('/user/email/reset', methods=['PUT', 'GET'])
@login_required
def reset_email_view():
    if request.method == 'PUT':
        form = ChangeEmailValidate().validate_api()
        user = User.validate_code(form)
        user.update(email=form.email.data)
        send_validate_email_email(user=user, form=form)
        return generate_res()
    uid = get_jwt_identity()
    code, user = User.set_code_by(uid=uid)
    send_change_email_email(code=code, user=user)
    return generate_res()


@admin.route('/user/email/add', methods=['POST'])
@login_required
def add_email_view():
    uid = get_jwt_identity()
    form = EmailValidate().validate_api()
    send_validate_email_email(uid=uid, form=form)
    return generate_res()


# 新邮箱token验证
@admin.route('/user/email/auth/<string:token>')
def auth_email_view(token):
    res = confirm_email_token(token)
    claims, id_ = get_attr(['user_claims', 'id'], res)
    User.update_by_id(id_=id_, email_is_validate=True)
    add_token_to_blacklist(token)
    return generate_res()
