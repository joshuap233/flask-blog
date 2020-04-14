from flask import current_app
from flask_mail import Mail
from flask_mail import Message

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


def send_register_success_email(email):
    send_email(
        to=email,
        subject='注册成功',
        content='注册成功'
    )


def send_change_email_success_email(email):
    send_email(
        to=email,
        subject='修改邮箱成功',
        content='修改邮箱成功'
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
