from flask import request, url_for

from .blueprint import admin
from app.database import User
from app.utils import generate_res, required_login, get_attr, send_email


@admin.route('/auth/register/', methods=['POST'])
def admin_register():
    data = request.get_json()
    if data.get('phone'):
        data['phone'] = str(data['phone'])
    email, username, nickname, password = get_attr(['email', 'username', 'nickname', 'password'], data)
    if username and password and nickname and email:
        user = User()
        user.set_attrs(data)
        user.generate_password_hash(password)
        user.auto_add()
        # TODO: 验证邮件是否发送成功
        send_email(data['email'], '账号注册', url_for('admin.admin_auth_email', token=user.generate_token()))
        return generate_res('success', 'register')
    return generate_res('failed', 'password, username, email,nickname, could not be empty')


@admin.route('/admin/auth/register/<string:token>')
def admin_auth_email(token):
    pass


@admin.route('/admin/auth/login/', methods=['POST'])
def admin_login():
    username, password = get_attr(['username', 'password'], request.get_json())
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        user.is_active = True
        user.auto_add()
        return generate_res('success', 'login', id=user.id, token=user.generate_token(), expiration=3600)


@admin.route('/admin/auth/logout/', methods=["DELETE"])
@required_login
def admin_logout():
    uid = request.headers.get('identify')
    user = User.query.filter_by(id=uid).first()
    user.is_active = False
    user.auto_add()
    return generate_res('success', 'logout')
