from flask_cors import CORS
from flask_mongoengine import MongoEngine
from flask_mail import Mail, Message
from flask_apscheduler import APScheduler


db = MongoEngine()

CORS(supports_credentials=True)

mail = Mail()

schedule = APScheduler()


def configExtensions(app):
    db.init_app(app)
    mail.init_app(app)
    CORS(app)
    schedule.init_app(app)
    schedule.start()
