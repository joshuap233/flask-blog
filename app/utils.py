import time

from flask import jsonify, current_app
from app.exception import ParameterException
from secrets import randbelow
import datetime
from app.config.constant import VERIFICATION_CODE_LENGTH


def time2stamp(time_, format_='%Y/%m/%d %H:%M') -> int:
    from wtforms.validators import StopValidation
    try:
        return int(time.mktime(time.strptime(time_, format_)))
    except:
        # 停止验证
        raise StopValidation(message="日期格错误")


def format_time(timestamp: int, format_='%Y/%m/%d %H:%M'):
    return time.strftime(format_, time.localtime(timestamp))


def generate_res(status='success', **kwargs):
    status = {
        'status': status,
    }
    status.update(kwargs)
    return jsonify(status)


def get_attr(keys: list, data: dict) -> list:
    return [data.get(key) for key in keys]


def filters_filename(file) -> str:
    from uuid import uuid1
    ext_name = file.content_type.split('/')[1]
    if ext_name not in current_app.config['ALLOWED_EXTENSIONS']:
        raise ParameterException('扩展名错误')
    return f'{str(uuid1())}.{ext_name}'


def generate_verification_code() -> str:
    code = ''
    for i in range(VERIFICATION_CODE_LENGTH):
        code += str(randbelow(9))
    return code


def get_now_timestamp() -> int:
    return int(datetime.datetime.now().timestamp())


def get_code_exp_stamp() -> int:
    now = datetime.datetime.now()
    expire_time = now + current_app.config['VERIFICATION_CODE_EXPIRE']
    return int(expire_time.timestamp())
