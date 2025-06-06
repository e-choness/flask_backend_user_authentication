import random
from app.models.user import User
from app.models.basicInfo import BasicInfo
from app.config.baseConfig import Config


def initDataBase():
    createTemplatesUser(Config.TEMPALTES_MANAGER)
    createBasicInfo()


def createTemplatesUser(managerName):
    randomPassWd = str(random.randint(100000, 999999))
    templateUser = User.objects.filter(userName=managerName).first()
    if not templateUser:
        User().userRegister(managerName, randomPassWd)


def createBasicInfo():
    basicinfo = BasicInfo.objects.first()
    if not basicinfo:
        BasicInfo.initBasicInfo()
