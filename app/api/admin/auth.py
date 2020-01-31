from flask import request, url_for

from app.model.db import User
from app.utils import generate_res, login_required, get_attr, send_email
from .blueprint import admin


@admin.route('/auth/register/', methods=['POST'])
def register_view():
    data = request.get_json()
    if data.get('phone'):
        data['phone'] = str(data['phone'])
    email, username, nickname, password = get_attr(['email', 'username', 'nickname', 'password'], data)
    if username and password and nickname and email:
        user = User()
        user.set_attrs(data)
        user.auto_add()
        # TODO: 验证邮件是否发送成功
        send_email(to=data['email'],
                   subject='账号注册',
                   content=url_for('admin.auth_register_view', token=user.generate_token()))
        return generate_res('success')
    return generate_res('failed', msg='password, username, email,nickname, could not be empty')


@admin.route('/auth/register/<string:token>')
def auth_register_view(token):
    status = User.confirm_register_token(token)
    return generate_res('success' if status else 'failed')


@admin.route('/auth/login/', methods=['POST'])
def login_view():
    username, password = get_attr(['username', 'password'], request.get_json())
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password) and user.is_validate:
        user.is_active = True
        user.auto_add()
        return generate_res('success', data={
            'id': user.id,
            'token': user.generate_token(),
        })
    return generate_res('failed')


@admin.route('/auth/logout/', methods=["DELETE"])
@login_required
def logout_view():
    uid = request.headers.get('identify')
    user = User.query.get(uid)
    user.is_active = False
    user.auto_add()
    return generate_res('success')


# 单独用于登录验证
@admin.route('/auth/')
@login_required
def auth_view():
    return generate_res('success', data={'auth': True})
