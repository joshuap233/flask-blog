from flask import Flask as _Flask
from flask.json import JSONEncoder as _JSONEncoder

from app.model.view_model import BaseView


class JSONEncoder(_JSONEncoder):
    def default(self, o):
        super(JSONEncoder, self).default(o)
        if isinstance(o, BaseView):
            return o.__dict__


class Flask(_Flask):
    json_encoder = JSONEncoder
