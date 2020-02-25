from flask import request
from wtforms import Form

from app.exception import ParameterException


class JsonValidate(Form):
    def __init__(self):
        data = request.get_json(silent=True)
        args = request.args.to_dict()
        super(JsonValidate, self).__init__(data=data, **args)

    def validate_api(self):
        valid = super(JsonValidate, self).validate()
        if not valid:
            raise ParameterException(msg=self.errors)
        return self
