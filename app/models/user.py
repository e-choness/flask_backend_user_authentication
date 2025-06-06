from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app
from app.api.error.exceptions import WrongPassword, WrongUserName
from app.extensions import db
from app.network.miniProgram import getUserOpenid


class User(db.Document):
    userName = db.StringField()

    passwordHash = db.StringField()

    email = db.StringField(max_length=30)

    isActive = db.BooleanField(default=True)

    miniProgramId = db.StringField()

    type = db.StringField()

    def getUserId(self):
        return str(self.id)

    @property
    def password(self):
        return self.passwordHash

    @password.setter
    def password(self, purePassword):
        self.passwordHash = generate_password_hash(purePassword)

    def registerByWechat(self, userName, openid):
        self.userName = userName
        self.miniProgramId = openid
        self.type = "MINI_PROGRAM_USER"
        self.save()

    def userRegister(self, userName, password):
        self.userName = userName
        self.password = password
        self.type = "WEB_USER"
        self.save()

    def checkPassword(self, purePassword):
        return check_password_hash(self.passwordHash, purePassword)

    @staticmethod
    def userLogin(userName, password):
        user = User.objects.filter(userName=userName).first()
        if not user:
            raise WrongUserName
        if not user.checkPassword(password):
            raise WrongPassword
        return user

    @staticmethod
    def userLoginByWeChat(userName, code):
        oid = getUserOpenid(code)
        u = User.objects.filter(miniProgramId=oid).first()
        if not u:
            User().registerByWechat(userName, oid)
        newU = User.objects.filter(miniProgramId=oid).first()
        return newU

    @staticmethod
    def getTemplateUserId():
        name = current_app.config['TEMPALTES_MANAGER']
        return str(User.objects.filter(userName=name).first().id)
