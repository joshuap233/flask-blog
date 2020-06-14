from threading import Thread

import yagmail

from app.config.config import MAIL_PASSWORD, MAIL_USERNAME, MAIL_PORT, MAIL_SERVER, MAIL_USE_SSL


class FakeMail:
    def send(self, *args, **kwargs):
        pass


if MAIL_USERNAME and MAIL_PASSWORD:
    yag = yagmail.SMTP(
        user=MAIL_USERNAME,
        password=MAIL_PASSWORD,
        host=MAIL_SERVER,
        port=MAIL_PORT,
        smtp_ssl=MAIL_USE_SSL
    )
else:
    yag = FakeMail()


def send_async_email(mail_param):
    # with app.app_context():
    yag.send(**mail_param)


def send_email(to, subject, content):
    # app = current_app._get_current_object()
    mail_param = dict(
        to=to,
        subject=subject,
        contents=[content]
    )
    t = Thread(target=send_async_email, args=[mail_param])
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
