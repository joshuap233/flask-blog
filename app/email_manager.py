from flask import url_for, current_app
from flask_jwt_extended import create_access_token
from flask_mail import Message
from flask_mail import Mail

mail = Mail()


# TODO :
# 判断邮箱是否验证

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


def send_validate_new_email_email(email, code):
    send_email(
        to=email,
        subject='新邮件地址验证',
        content=code
    )


def send_change_pass_warn(email):
    send_email(
        to=email,
        subject='您已修改密码',
        content='您已修改密码'
    )


def send_change_email_email(email, code):
    send_email(
        to=email,
        subject='邮箱地址修改确认',
        content=code
    )


def send_recovery_pass_email(email, code):
    send_email(
        to=email,
        subject='修改密码',
        content=code
    )
