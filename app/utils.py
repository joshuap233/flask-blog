import datetime
import os
import time
from secrets import randbelow

from flask import jsonify, current_app

from app.config.constant import VERIFICATION_CODE_LENGTH
from app.exception import NotFound
from app.exception import ParameterException
from app.myType import FileStorage


def time2stamp(time_: str, format_: str = '%Y/%m/%d %H:%M') -> int:
    from wtforms.validators import StopValidation
    try:
        return int(time.mktime(time.strptime(time_, format_)))
    except Exception as e:
        # 停止验证
        raise StopValidation(message="日期格错误")


def format_time(timestamp: int, format_: str = '%Y/%m/%d %H:%M'):
    return time.strftime(format_, time.localtime(timestamp))


def generate_res(status: str = 'success', **kwargs):
    status = {
        'status': status,
    }
    status.update(kwargs)
    return jsonify(status)


def get_attr(keys: list, data: dict) -> list:
    return [data.get(key) for key in keys]


def filters_filename(file: FileStorage) -> str:
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


def security_remove_file(path: str):
    try:
        os.remove(os.path.join(current_app.config['UPLOAD_FOLDER'], path))
    except FileNotFoundError:
        raise NotFound('文件不存在')
