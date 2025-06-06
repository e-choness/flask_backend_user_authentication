from wtforms import Form
from flask import request
from app.api.error.exceptions import ParameterException


class BaseForm(Form):
    def __init__(self):
        self.jsonData = request.json
        args = request.args.to_dict()
        if request.json:
            self.jsonKeys = request.json.keys()
        super().__init__(data=self.jsonData, **args)

    def validateForApi(self):
        validate = super(BaseForm, self).validate()
        if not validate:
            # 取第一眼验证错误的错误信息
            error = list(self.errors.values())[0][0]
            raise ParameterException(information=error)
        return self
