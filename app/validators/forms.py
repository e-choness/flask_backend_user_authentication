from wtforms import StringField, BooleanField, DateTimeField, IntegerField
from app.api.error.exceptions import SameUser, ParameterException, WrongType
from app.config.enums import UserTypeEnum
from app.models.user import User
from app.validators.base import BaseForm
from wtforms.validators import DataRequired, Length


class UserForm(BaseForm):
    userName = StringField(validators=[DataRequired(message="用户名不得为空")])
    secret = StringField(validators=[DataRequired(message="密码不得为空")])
    type = IntegerField(validators=[DataRequired(message="客户端类型不得为空")])

    def validate_type(self, field):
        try:
            userType = UserTypeEnum(field.data)
        except:
            raise WrongType
        self.type.data = userType


class MiniProgramLoginForm(UserForm):
    userName = StringField(validators=[DataRequired(message="用户名不得为空")])
    secret = StringField(validators=[DataRequired(message="code不得为空")])


class WebRegisterForm(UserForm):
    @staticmethod
    def validate_userName(form, field):
        currentUser = field.data
        user = User.objects.filter(userName=currentUser).first()
        if user:
            raise SameUser


class QuestionnaireForm(BaseForm):
    isSecret = BooleanField()
    secretKey = StringField()
    condition = BooleanField()
    title = StringField(
        validators=[Length(max=18, min=0, message="问卷标题长度必须小于%(max)d")])
    subTitle = StringField()
    wechatControl = BooleanField()
    ipControl = BooleanField()
    equipmentControl = BooleanField()
    deadlineControl = BooleanField()
    deadline = DateTimeField()
    renewTime = DateTimeField()

    questionnaireId = IntegerField(
        validators=[DataRequired(message="目标问卷id不得为空")])


class DeleteQuestionnaireForm(BaseForm):
    questionnaireId = IntegerField(
        validators=[DataRequired(message="目标问卷id不得为空")])


class ProblemForm(BaseForm):
    title = StringField(validators=[DataRequired(message="问题标题不得为空")])
    type = StringField(validators=[DataRequired(message="问题类型不得为空")])
    isRequire = BooleanField()
    targetQuestionnaireId = StringField(
        validators=[DataRequired(message="对应问卷id不得为空")])


class EditProblemForm(BaseForm):
    title = StringField()
    type = StringField()
    isRequire = BooleanField()
    problemId = IntegerField(validators=[DataRequired(message="目标问题id不得为空")])


class DeleteProblemForm(BaseForm):
    problemId = IntegerField(validators=[DataRequired(message="目标问题id不得为空")])


class QuestionireSecretCheckForm(BaseForm):
    secretKey = StringField(validators=[DataRequired(message="问卷密码不得为空")])


class QuestionnaireCompleteForm(BaseForm):
    pass


class GetTemplatesForm(BaseForm):
    page = IntegerField(validators=[DataRequired(message="页码不得为空")])

    @staticmethod
    def validate_page(form, field):
        try:
            page = int(field.data)
        except:
            raise ParameterException


class CopyTemplatesForm(BaseForm):
    templateId = IntegerField(validators=[DataRequired(message="id不得为空")])
