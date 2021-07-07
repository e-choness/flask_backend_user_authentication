from flask import request, current_app

from app.utils.code import ResponseCode


class ResMsg(object):
    """
    responser wrapper
    """

    def __init__(self, data=None, code=ResponseCode.Success, rq=request):
        self.lang = rq.headers.get("lang",
                                   current_app.config.get("LANG", "zh_CN")
                                   )
        self._data = data
        self._msg = current_app.config[self.lang].get(code, None)
        self._code = code

    def update(self, code=None, data=None, msg=None):
        """
        :param code:
        :param data:
        :param msg:
        :return:
        """
        if code is not None:
            self._code = code
            self._msg = current_app.config[self.lang].get(code, None)
        if data is not None:
            self._data = data
        if msg is not None:
            self._msg = msg

    def add_field(self, name=None, value=None):
        """
        :param name:
        :param value:
        :return:
        """
        if name is not None and value is not None:
            self.__dict__[name] = value

    @property
    def data(self):
        """
        :return:
        """
        body = self.__dict__
        body["data"] = body.pop("_data")
        body["msg"] = body.pop("_msg")
        body["code"] = body.pop("_code")
        return body
