import uuid
from flask import current_app
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest

from app.models.model import UserLoginMethod, User
from app.utils.core import db


# smss = {
#     "SMS_ACCESS_KEY_ID": "128548974",  # key ID
#     "SMS_ACCESS_KEY_SECRET": "323232",  #
#     "SMS_SIGN_NAME": "Signature_Setting",  #
#     "AUTHENTICATION": "SMS_1551323",  #
#     "LOGIN_CONFIRMATION": "SMS_155546",  #
#     "LOGIN_EXCEPTION": "SMS_1556546",  #
#     "USER_REGISTRATION": "SMS_1551654625",  #
#     "CHANGE_PASSWORD": "SMS_155126456",  #
#     "INFORMATION_CHANGE": "SMS_1551265463",  #
# }


class SendSms(object):

    def __init__(self, phone: str = None, category: str = None, template_param=None):
        """

        :param phone: 
        :param category: 
        :param template_param: 
        """
        access_key_id = current_app.config.get('SMS_ACCESS_KEY_ID', None)
        access_key_secret = current_app.config.get(
            'SMS_ACCESS_KEY_SECRET', None)
        sign_name = current_app.config.get("SMS_SIGN_NAME", None)

        if access_key_id is None:
            raise ValueError("miss message key")

        if access_key_secret is None:
            raise ValueError("miss message secret")

        if phone is None:
            raise ValueError("phone number error")

        if template_param is None:
            raise ValueError("message template error")

        if category is None:
            raise ValueError("message encode error")

        if sign_name is None:
            raise ValueError("message signature error")

        self.acs_client = AcsClient(access_key_id, access_key_secret)
        self.phone = phone
        self.category = category
        self.template_param = template_param
        self.template_code = self.template_code()
        self.sign_name = sign_name

    def template_code(self):
        """
        :param self.category
           authentication: 
           login_confirmation: 
           login_exception: 
           user_registration: 
           change_password:
           information_change:
        :return:
        """
        if self.category == "authentication":
            code = current_app.config.get('AUTHENTICATION', None)
            if code is None:
                raise ValueError("NOT FOUND AUTHENTICATION")
            return code

        elif self.category == "login_confirmation":
            code = current_app.config.get('LOGIN_CONFIRMATION', None)
            if code is None:
                raise ValueError("NOT FOUND LOGIN_CONFIRMATION")
            return code
        elif self.category == "login_exception":
            code = current_app.config.get('LOGIN_EXCEPTION', None)
            if code is None:
                raise ValueError("NOT FOUND LOGIN_EXCEPTION")
            return code
        elif self.category == "user_registration":
            code = current_app.config.get('USER_REGISTRATION', None)
            if code is None:
                raise ValueError("NOT FOUND USER_REGISTRATION")
            return code
        elif self.category == "change_password":
            code = current_app.config.get('CHANGE_PASSWORD', None)
            if code is None:
                raise ValueError("NOT FOUND CHANGE_PASSWORD")
            return code
        elif self.category == "information_change":
            code = current_app.config.get('INFORMATION_CHANGE', None)
            if code is None:
                raise ValueError("NOT FOUND INFORMATION_CHANGE")
            return code
        else:
            raise ValueError("message code invalid")

    def send_sms(self):
        """
        :return:
        """

        sms_request = CommonRequest()

        # fixed setting
        sms_request.set_accept_format('json')
        sms_request.set_domain('dysmsapi.aliyuncs.com')
        sms_request.set_method('POST')
        sms_request.set_protocol_type('https')  # https | http
        sms_request.set_version('2017-05-25')
        sms_request.set_action_name('SendSms')

        sms_request.add_query_param('PhoneNumbers', self.phone)
        sms_request.add_query_param('SignName', self.sign_name)

        sms_request.add_query_param('TemplateCode', self.template_code)

        sms_request.add_query_param('TemplateParam', self.template_param)

        build_id = uuid.uuid1()
        sms_request.add_query_param('OutId', build_id)

        sms_response = self.acs_client.do_action_with_exception(sms_request)

        return sms_response


def phone_login_or_register(phone):
    """
    :param phone:
    :return:
    """
    user_login = db.session(UserLoginMethod). \
        filter(UserLoginMethod.login_method == "P",
               UserLoginMethod.identification == phone, ).first()

    if user_login:
        user = db.session.query(User.id, User.name).filter(
            User.id == user_login.user_id).first()
        data = dict(zip(user.keys(), user))
        return data
    else:
        try:
            new_user = User(name="nickname", age=20)
            db.session.add(new_user)
            db.session.flush()
            new_user_login = UserLoginMethod(user_id=new_user.id,
                                             login_method="P",
                                             identification=phone,
                                             access_code=None)
            db.session.add(new_user_login)
            db.session.flush()
            db.session.commit()
        except Exception as e:
            print(e)
            return None

        data = dict(id=new_user.id, name=User.name)
        return data
