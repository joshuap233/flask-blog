import datetime
import os
import time
from secrets import randbelow

from flask import jsonify, current_app, request

from app.config.constant import VERIFICATION_CODE_LENGTH
from app.exception import NotFound
from app.exception import ParameterException
from app.myType import FileStorage
import base64
from uuid import uuid1
from mimetypes import guess_extension
import imghdr


def save_base64_img(base64_string) -> str:
    if base64_string == '':
        return ''
    # 去除'data: 字符串"
    base64_string = base64_string[5:]
    img = base64.b64decode(base64_string.split(',', 1)[1])
    path = current_app.config['UPLOAD_FOLDER']
    filename = str(uuid1())

    try:
        img_ext = guess_extension(base64_string.split(';')[0])
        if img_ext[1:] not in current_app.config['ALLOWED_EXTENSIONS']:
            raise ParameterException('扩展名错误')
    except Exception as e:
        raise ParameterException('扩展名错误')

    filename = filename + img_ext
    path = os.path.join(path, filename)
    with open(path, 'wb') as f:
        f.write(img)
    return filename


def save_img() -> str:
    # TODO: 文件校验(svg过滤,压缩处理
    path = current_app.config['UPLOAD_FOLDER']
    img = request.files.get('image')
    filename = filters_filename(img)
    img.save(os.path.join(path, filename))
    return filename


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
    ext_name = guess_extension(file.content_type)
    if ext_name[1:] not in current_app.config['ALLOWED_EXTENSIONS']:
        raise ParameterException('扩展名错误')
    return f'{str(uuid1())}{ext_name}'


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
        pass
        # raise NotFound('文件不存在')


def create_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)
