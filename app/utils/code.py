class ResponseCode(object):
    Success = 0  
    Fail = -1  
    NoResourceFound = 40001  
    InvalidParameter = 40002  
    AccountOrPassWordErr = 40003 
    VerificationCodeError = 40004  
    PleaseSignIn = 40005  
    WeChatAuthorizationFailure = 40006 
    InvalidOrExpired = 40007  
    MobileNumberError = 40008  
    FrequentOperation = 40009


class ResponseMessage(object):
    Success = "success"
    Fail = "fail"
    NoResourceFound = "no resource found"
    InvalidParameter = "invalid parameter"
    AccountOrPassWordErr = "account or password error"
    VerificationCodeError = "verification code error"
    PleaseSignIn = "please login"
