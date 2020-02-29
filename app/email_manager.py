from flask import url_for, current_app
from flask_jwt_extended import create_access_token
from flask_mail import Message
from flask_mail import Mail

mail = Mail()


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(to, subject, content):
    from threading import Thread
    app = current_app._get_current_object()
    msg = Message(
        subject=subject,
        sender=current_app.config['MAIL_USERNAME'],
        recipients=[to]
    )
    msg.body = content
    # msg.html = "<b>testing</b>"
    t = Thread(target=send_async_email, args=[app, msg])
    t.start()


# 添加新邮件
def send_validate_email_email(user=None, uid=None, form=None, addr=None):
    email = addr if addr else form.email.data
    uid = uid if uid else user.id
    send_email(
        to=email,
        subject='新邮件确认',
        content=url_for(
            'admin.auth_email_view',
            token=create_access_token(identity=uid, user_claims={'email': email})
        ))


def send_change_email_email(user, code):
    send_email(
        to=user.email,
        subject='邮箱地址修改确认',
        content=code
    )


def send_forget_password_email(form, code):
    send_email(
        to=form.email.data,
        subject='修改密码',
        content=code
    )


def send_change_password_warn(user):
    send_email(
        to=user.id,
        subject='密码已修改',
        content='密码已修改'
    )
