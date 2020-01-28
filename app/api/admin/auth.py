from flask import request, url_for

from app.model.db import User
from app.utils import generate_res, login_required, get_attr, send_email
from .blueprint import admin


@admin.route('/auth/register/', methods=['POST'])
def admin_register():
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
                   content=url_for('admin.admin_auth_register', token=user.generate_token()))
        return generate_res('success', 'register')
    return generate_res('failed', 'password, username, email,nickname, could not be empty')


@admin.route('/auth/register/<string:token>')
def admin_auth_register(token):
    status = User.confirm_register_token(token)
    return generate_res('success' if status else 'failed', '')


@admin.route('/auth/login/', methods=['POST'])
def admin_login():
    username, password = get_attr(['username', 'password'], request.get_json())
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password) and user.is_validate:
        user.is_active = True
        user.auto_add()
        return generate_res('success', 'login', id=user.id, token=user.generate_token(), expiration=3600)


@admin.route('/auth/logout/', methods=["DELETE"])
@login_required
def admin_logout():
    uid = request.headers.get('identify')
    user = User.query.get(uid)
    user.is_active = False
    user.auto_add()
    return generate_res('success', 'logout')
