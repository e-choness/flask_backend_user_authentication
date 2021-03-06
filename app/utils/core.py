import datetime
import decimal
import uuid

from flask.json import JSONEncoder as BaseJSONEncoder
from flask_sqlalchemy import SQLAlchemy
from flask_apscheduler import APScheduler

scheduler = APScheduler()

db = SQLAlchemy()


class JSONEncoder(BaseJSONEncoder):

    def default(self, o):
        """
        :param o:
        :return:
        """
        if isinstance(o, datetime.datetime):
            return o.strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(o, datetime.date):
            return o.strftime('%Y-%m-%d')
        if isinstance(o, decimal.Decimal):
            return str(o)
        if isinstance(o, uuid.UUID):
            return str(o)
        if isinstance(o, bytes):
            return o.decode("utf-8")
        return super(JSONEncoder, self).default(o)
