from app.api.error.baseHandler import JobException


class WrongPassword(JobException):
    code = 403
    errorCode = "error"
    information = "Invalid username or password"


class WrongCheckCode(JobException):
    code = 403
    errorCode = "error"
    information = "Invalid authentication code"


class SameUser(JobException):
    code = 403
    errorCode = "error"
    information = "The username already exists"


class WrongUserName(JobException):
    code = 403
    errorCode = "error"
    information = "The username does not exist"


class WrongAuth(JobException):
    code = 403
    errorCode = "error"
    information = "Invalid permission"


class ParameterException(JobException):
    code = 403
    errorCode = "validate error"
    information = "Authentication failed"


class NoQuestionnaire(JobException):
    code = 404
    errorCode = "no quesitionnaire"
    information = "Sorry, the questionnaire does not exist"


class NoProblem(JobException):
    code = 404
    errorCode = "no problem"
    information = "Sorry, the problem does not exist"


class WrongProblemSecretKey(JobException):
    code = 404
    errorCode = "wrong skey"
    information = "Sorry, the problem secret key is incorrect"


class SameIp(JobException):
    code = 403
    errorCode = "error"
    information = "The user IP has already submitted the questionnaire, please do not submit again"


class WrongType(JobException):
    code = 403
    errorCode = "error"
    information = "Invalid client type"


class WrongCode(JobException):
    code = 403
    errorCode = "error"
    information = "Invalid user code"
