from flask import Flask
from app.config.baseConfig import ProductionConfig, DevelopmentConfig
from app.api import configBlueprint
from app.config.database import initDataBase
from app.extensions import configExtensions


def createApp():

    app = Flask(__name__)

    app.config.from_object(DevelopmentConfig)

    configBlueprint(app)

    configExtensions(app)

    initDataBase()

    return app
