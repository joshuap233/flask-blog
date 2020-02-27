from flask import url_for
from app.utils import send_email
from flask_jwt_extended import decode_token
from app.model.db import User


def send_register_email(form, user):
    send_email(
        to=form.email.data,
        subject='账户邮件修改确认',
        content=url_for('admin.auth_email_view', token=user.generate_access_token())
    )


def send_change_email_email(form, user):
    send_email(
        to=form.email.data,
        subject='账户邮件修改确认',
        content=url_for('admin.auth_email_view', token=user.generate_access_token())
    )


def confirm_email_token(token):
    res = decode_token(token)
    id_ = res.get('identity')
    User.update_by_id(id_, email_is_validate=True)
