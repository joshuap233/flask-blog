from flask import request

from app.model.db import User
from app.model.view_model import UserInfoView, LoginView
from app.utils import generate_res, get_attr
from app.validate.validate import (
    RegisterValidate, UserValidate, LoginValidate,
    EmailValidate, ForgetPasswordValidate, ResetPasswordValidate)
from .blueprint import admin
from flask_jwt_extended import get_jwt_identity
from app.email_manager import (
    send_validate_email_email, send_change_email_email,
    MailType, send_change_password_warn, forget_password_email)
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
    user = User.query.get_or_404(uid)
    if request.method == 'PUT':
        form = UserValidate().validate_api()
        user.update(form.data)
        return generate_res()
    return generate_res(data=UserInfoView(user))


@admin.route('/user/password/forget', methods=['POST', 'GET'])
def forget_password_view():
    form = EmailValidate().validate_api()
    if request.method == 'POST':
        form = ForgetPasswordValidate().validate_api()
    code = User.set_ver_code(form)
    forget_password_email(form=form, code=code)
    return generate_res()


@admin.route('/user/password/reset', methods=['POST'])
@login_required
def reset_password_view():
    form = ResetPasswordValidate().validate_api()
    user = User.reset_password(form)
    send_change_password_warn(user=user)
    return generate_res()


# 邮箱用于登录/修改密码验证
@admin.route('/user/email', methods=['PUT'])
@login_required
def add_or_reset_email_view():
    form = EmailValidate().validate_api()
    id_ = get_jwt_identity()
    user = User.query.get_or_404(id_)
    if user.is_change_email(form):
        send_change_email_email(uid=id_, form=form)
    else:
        send_validate_email_email(uid=id_, form=form)
    return generate_res()


@admin.route('/user/email/auth/<string:token>')
def auth_email_view(token):
    res = confirm_email_token(token)
    claims, id_ = get_attr(['user_claims', 'id'], res)
    email, mail_type = get_attr(['email', 'type'], claims)
    if mail_type == MailType.CHANGE_EMAIL.value:
        send_validate_email_email(uid=id_, addr=email)
    elif mail_type == MailType.NEW_EMAIL.value:
        User.update_email_by_id(uid=id_, email=email)
        add_token_to_blacklist(token)
    return generate_res()
