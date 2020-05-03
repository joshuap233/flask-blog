from flask import Flask as _Flask, Blueprint
from flask.json import JSONEncoder

from app.config.security import API_SECURITY_STRING
from app.model.baseView import BaseView
from app.myType import Any
import os


class MyBlueprint(Blueprint):
    def route(self, rule: str, **options):
        if API_SECURITY_STRING and os.getenv('FLASK_ENV') == 'production':
            rule = f'/{API_SECURITY_STRING}{rule}'
        return super(MyBlueprint, self).route(rule, **options)


class MyJSONEncoder(JSONEncoder):
    def default(self, o: Any):
        if isinstance(o, BaseView):
            return o.__dict__
        super().default(o)


class Flask(_Flask):
    json_encoder = MyJSONEncoder
