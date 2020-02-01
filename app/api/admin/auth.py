from flask import request, url_for

from app.model.db import User
from app.model.view_model import JsonToUserView
from app.utils import generate_res, login_required, send_email
from .blueprint import admin


@admin.route('/auth/register/', methods=['POST'])
def register_view():
    new_user = JsonToUserView(request.get_json())
    # TODO: 添加手机验证
    if new_user.type == 'email' and new_user.email:
        user = User.query.get(new_user.id)
        if not user:
            return generate_res('failed', msg='user not found')
        user.email = user.email
        user.auto_add()
        # TODO: 验证邮件是否发送成功
        send_email(to=new_user.email,
                   subject='账号注册',
                   content=url_for('admin.auth_register_view', token=user.generate_token()))
        return generate_res('success')

    elif new_user.type == 'username':
        user = User()
        user.set_attrs(new_user.fill())
        user.auto_add()
        return generate_res('success', data={'userId': user.id})
    return generate_res('failed', msg='field empty')


@admin.route('/auth/register/<string:token>')
def auth_email_view(token):
    status = User.confirm_email_token(token)
    return generate_res('success' if status else 'failed')


@admin.route('/auth/login/', methods=['POST'])
def login_view():
    # 添加手机登录,邮箱验证码登录
    user_data = JsonToUserView(request.get_json())
    if not user_data.query:
        return generate_res('failed')
    user = User.query.filter_by(**user_data.query).first()
    if user and user.check_password(user_data.password):
        user.is_active = True
        user.auto_add()
        return generate_res('success', data={
            'id': user.id,
            'token': user.generate_token(),
        })
    return generate_res('failed'), 401


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
    return generate_res('success')
