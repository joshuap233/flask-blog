from flask import request, url_for

from app.exception import AuthFailed
from app.model.db import User
from app.model.view_model import UserInfoView
from app.utils import generate_res, login_required, send_email
from app.validate.validate import RegisterValidate, UserValidate, LoginValidate
from .blueprint import admin


@admin.route('/auth/register', methods=['POST'])
def register_view():
    form = RegisterValidate().validate_api()
    user = User.create(form.data)
    if form.email:
        send_email(
            to=form.email,
            subject='账号注册',
            content=url_for('admin.auth_register_view', token=user.generate_token())
        )
    return generate_res()


@admin.route('/auth/user/info', methods=["GET", "PUT"])
@login_required
def user_info_view():
    uid = request.headers.get('identify')
    user = User.query.get_or_404(uid)
    if request.method == 'PUT':
        form = UserValidate().validate_api()
        if form.email.data and form.email.data != user.email:
            user.email_is_validate = False
            user.email = form.email.data
            send_email(
                to=form.email,
                subject='邮件修改确认',
                content=url_for('admin.auth_register_view', token=user.generate_token())
            )
        user.update(form.data)
        return generate_res()
    return generate_res(data=UserInfoView(user))


@admin.route('/auth/register/<string:token>')
def auth_email_view(token):
    User.confirm_email_token(token)
    return generate_res()


@admin.route('/auth/login', methods=['POST'])
def login_view():
    form = LoginValidate().validate_api()
    user = User.query.filter_by(username=form.username.data).first_or_404()
    if not user.check_password(form.password.data):
        raise AuthFailed()
    user.update(is_active=True)
    return generate_res(data={
        'id': user.id,
        'token': user.generate_token(),
    })


@admin.route('/auth/logout', methods=["DELETE"])
@login_required
def logout_view():
    uid = request.headers.get('identify')
    User.update_by_id(uid, is_active=False)
    return generate_res()


# 单独用于登录验证
@admin.route('/auth')
@login_required
def auth_view():
    return generate_res()
