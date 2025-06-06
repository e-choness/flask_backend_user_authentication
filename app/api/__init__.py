from app.api.error.baseHandler import commonException
from app.api.v1 import configBluePrintV1

# This file is part of the OpenJudge project.


def configBlueprint(app):
    app.register_blueprint(configBluePrintV1(), url_prefix='/v1')
    app.register_blueprint(commonException)
