from app.utils.templateMaker.templateMaker import pushWJWDataToDB


class Config:

    SECRET_KEY = 'your_secret_key_here'

    JSON_AS_ASCII = False

    TOKEN_EXPIRATION = 7200

    MAIL_SERVER = 'your_server_mail'
    MAIL_USERNAME = 'your_username'
    MAIL_PASSWORD = 'your_password'
    MAIL_PORT = 465
    MAIL_DEFAULT_SENDER = 'your_default_sender'
    MAIL_USE_SSL = True
    MAIL_USE_TLS = False

    ADMIN_EMAIL = "admin_email"

    TEMPALTES_MANAGER = "TEMPLATE_MAKER"

    MINI_PROGRAM_APPID = "appid"
    MINI_PROGRAM_APPSECRET = "appsecret"


class DevelopmentConfig(Config):

    MONGODB_SETTINGS = {
        'db': '',
        'host': ''
    }

    WEB_BASE_URL = "http://192.168.0.129:8080"


class ProductionConfig(Config):

    MONGODB_SETTINGS = {
        'db': 'questionnaire',
        'host': 'mongodb://localhost/questionnaire'
    }

    WEB_BASE_URL = ""

    SCHEDULER_API_ENABLED = True
    JOBS = [
        {
            "id": "runTask",
            "func": pushWJWDataToDB,
            "trigger": "cron",
            "hour": '16',
            "minute": '38'
        }
    ]
