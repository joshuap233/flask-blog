from flask import Flask as _Flask, Blueprint
from flask.json import JSONEncoder

from app.config.config import API_SECURITY_STRING
from app.model.view import BaseView
from app.myType import Any


def is_security(options):
    return API_SECURITY_STRING and options.pop('security', True)


class MyBlueprint(Blueprint):
    def route(self, rule: str, **options):
        if is_security(options):
            rule = f'/{API_SECURITY_STRING}{rule}'
        return super(MyBlueprint, self).route(rule, **options)


class MyJSONEncoder(JSONEncoder):
    def default(self, o: Any):
        if isinstance(o, BaseView):
            return o.__dict__
        super().default(o)


class Flask(_Flask):
    json_encoder = MyJSONEncoder
