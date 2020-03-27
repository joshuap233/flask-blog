from flask import Flask as _Flask
from flask.json import JSONEncoder

from app.model.baseView import BaseView


class MyJSONEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, BaseView):
            return o.__dict__
        super().default(o)


class Flask(_Flask):
    json_encoder = MyJSONEncoder
