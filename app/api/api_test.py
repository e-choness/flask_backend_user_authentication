import logging
import random
import uuid
import os
from flask import Blueprint, jsonify, session, request, current_app
from datetime import datetime, timedelta
from decimal import Decimal

from app.api.tree import Tree
from app.utils.code import ResponseCode
from app.utils.response import ResMsg
from app.utils.util import route, Redis, CaptchaTool, PhoneTool
from app.utils.auth import Auth, login_required
from app.api.report import excel_write, word_write, pdf_write
from app.api.wx_login_or_register import get_access_code, get_wx_user_info, wx_login_or_register
from app.api.phone_login_or_register import SendSms, phone_login_or_register
from app.celery import add, flask_app_context

bp = Blueprint("test", __name__, url_prefix='/')

logger = logging.getLogger(__name__)


# -----------------Route for BluePrint---------------#


@bp.route('/logs', methods=["GET"])
def test_logger():
    """
    test logger
    :return:
    """
    logger.info("this is info")
    logger.debug("this is debug")
    logger.warning("this is warning")
    logger.error("this is error")
    logger.critical("this is critical")
    return "ok"


@bp.route("/unifiedResponse", methods=["GET"])
def test_unified_response():
    """
    test response wrapper
    :return:
    """
    res = ResMsg()
    test_dict = dict(name="zhang", age=18)
    res.update(code=ResponseCode.Success, data=test_dict)
    return jsonify(res.data)


# --------------Customized route for BluePrint--------------------#


@route(bp, '/packedResponse', methods=["GET"])
def test_packed_response():
    """
    test response wrapper
    :return:
    """
    res = ResMsg()
    test_dict = dict(name="zhang", age=18)
    # pass responseCode and data
    res.update(code=ResponseCode.Success, data=test_dict)
    # no need jsonify，if need to specify http code and header, as below
    # return res.data,200,{"token":"111"}
    return res.data


@route(bp, '/typeResponse', methods=["GET"])
def test_type_response():
    """
    test different response type
    :return:
    """
    res = ResMsg()
    now = datetime.now()
    date = datetime.now().date()
    num = Decimal(11.11)
    test_dict = dict(now=now, date=date, num=num)
    res.update(code=ResponseCode.Success, data=test_dict)
    # return res.data,200,{"token":"111"}
    return res.data


# --------------test Redis--------------------#

@route(bp, '/testRedisWrite', methods=['GET'])
def test_redis_write():
    """
    redis write
    """
    # write
    Redis.write("test_key", "test_value", 60)
    return "ok"


@route(bp, '/testRedisRead', methods=['GET'])
def test_redis_read():
    """
    redis read
    """
    data = Redis.read("test_key")
    return data


# -----------------Captcha---------------------------#

@route(bp, '/testGetCaptcha', methods=["GET"])
def test_get_captcha():
    """
    get captcha
    :return:
    """
    res = ResMsg()
    new_captcha = CaptchaTool()
    img, code = new_captcha.get_verify_code()
    res.update(data=img)
    session["code"] = code
    return res.data


@route(bp, '/testVerifyCaptcha', methods=["POST"])
def test_verify_captcha():
    """
    verify captcha
    :return:
    """
    res = ResMsg()
    obj = request.get_json(force=True)
    code = obj.get('code', None)
    s_code = session.get("code", None)
    print(code, s_code)
    if not all([code, s_code]):
        res.update(code=ResponseCode.InvalidParameter)
        return res.data
    if code != s_code:
        res.update(code=ResponseCode.VerificationCodeError)
        return res.data
    return res.data


# --------------------JWT test-----------------------------------------#

@route(bp, '/testLogin', methods=["POST"])
def test_login():
    """
    login -> get token & refresh token
    :return:
    """
    res = ResMsg()
    obj = request.get_json(force=True)
    user_name = obj.get("name")
    # not exist
    if not obj or not user_name:
        res.update(code=ResponseCode.InvalidParameter)
        return res.data

    if user_name == "qin":
        # generate jwt code based on usr id
        access_token, refresh_token = Auth.encode_auth_token(user_id=user_name)

        data = {"access_token": access_token.decode("utf-8"),
                "refresh_token": refresh_token.decode("utf-8")
                }
        res.update(data=data)
        return res.data
    else:
        res.update(code=ResponseCode.AccountOrPassWordErr)
        return res.data


@route(bp, '/testGetData', methods=["GET"])
@login_required
def test_get_data():
    """
    test jwt token
    :return:
    """
    res = ResMsg()
    name = session.get("user_name")
    data = "{}，Hello ！！".format(name)
    res.update(data=data)
    return res.data


@route(bp, '/testRefreshToken', methods=["GET"])
def test_refresh_token():
    """
    test refresh token
    :return:
    """
    res = ResMsg()
    refresh_token = request.args.get("refresh_token")
    if not refresh_token:
        res.update(code=ResponseCode.InvalidParameter)
        return res.data
    payload = Auth.decode_auth_token(refresh_token)
    # token is modified
    if not payload:
        res.update(code=ResponseCode.PleaseSignIn)
        return res.data

    # invalid token
    if "user_id" not in payload:
        res.update(code=ResponseCode.PleaseSignIn)
        return res.data
    # get new token
    access_token = Auth.generate_access_token(user_id=payload["user_id"])
    data = {"access_token": access_token.decode(
        "utf-8"), "refresh_token": refresh_token}
    res.update(data=data)
    return res.data


# --------------------test export Excel-------------------------------#

@route(bp, '/testExcel', methods=["GET"])
def test_excel():
    """
    test excel output
    :return:
    """
    res = ResMsg()
    report_path = current_app.config.get("REPORT_PATH", "./report")
    file_name = "{}.xlsx".format(uuid.uuid4().hex)
    path = os.path.join(report_path, file_name)
    path = excel_write(path)
    path = path.lstrip(".")
    res.update(data=path)
    return res.data


# --------------------test export Word-------------------------------#

@route(bp, '/testWord', methods=["GET"])
def test_word():
    """
    test export word
    :return:
    """
    res = ResMsg()
    report_path = current_app.config.get("REPORT_PATH", "./report")
    file_name = "{}.docx".format(uuid.uuid4().hex)
    path = os.path.join(report_path, file_name)
    path = word_write(path)
    path = path.lstrip(".")
    res.update(data=path)
    return res.data


# --------------------test directory-------------------------------#

@route(bp, '/testTree', methods=["GET"])
def test_tree():
    """
    test directory / menu
    :return:
    """
    res = ResMsg()
    data = [
        {"id": 1, "father_id": None, "name": "01"},
        {"id": 2, "father_id": 1, "name": "0101"},
        {"id": 3, "father_id": 1, "name": "0102"},
        {"id": 4, "father_id": 1, "name": "0103"},
        {"id": 5, "father_id": 2, "name": "010101"},
        {"id": 6, "father_id": 2, "name": "010102"},
        {"id": 7, "father_id": 2, "name": "010103"},
        {"id": 8, "father_id": 3, "name": "010201"},
        {"id": 9, "father_id": 4, "name": "010301"},
        {"id": 10, "father_id": 9, "name": "01030101"},
        {"id": 11, "father_id": 9, "name": "01030102"},
    ]

    new_tree = Tree(data=data)

    data = new_tree.build_tree()

    res.update(data=data)
    return res.data


# --------------------test Wechat-------------------------------#

@route(bp, '/testWXLoginOrRegister', methods=["GET"])
def test_wx_login_or_register():
    """
    test WeChat login
    :return:
    """
    res = ResMsg()
    code = request.args.get("code")
    flag = request.args.get("flag")
    # Parameter error
    if code is None or flag is None:
        res.update(code=ResponseCode.InvalidParameter)
        return res.data
    # Get Auth Code from WeChat
    access_code = get_access_code(code=code, flag=flag)
    if access_code is None:
        res.update(code=ResponseCode.WeChatAuthorizationFailure)
        return res.data
    # get WeChat user info
    wx_user_info = get_wx_user_info(access_data=access_code)
    if wx_user_info is None:
        res.update(code=ResponseCode.WeChatAuthorizationFailure)
        return res.data

    # validate if WeChat user exist or not，
    data = wx_login_or_register(wx_user_info=wx_user_info)
    if data is None:
        res.update(code=ResponseCode.Fail)
        return res.data
    res.update(data=data)
    return res.data


# --------------------test login by mobile phone verification code-------------------------------#

@route(bp, '/testGetVerificationCode', methods=["GET"])
def test_get_verification_code():
    """
    get_verification_code
    :return:
    """
    now = datetime.now()
    res = ResMsg()

    category = request.args.get("category", None)
    # category：
    # authentication
    # login_confirmation
    # login_exception
    # user_registration
    # change_password
    # information_change

    phone = request.args.get('phone', None)

    # check if the phone code correct or not
    re_phone = PhoneTool.check_phone(phone)
    if phone is None or re_phone is None:
        res.update(code=ResponseCode.MobileNumberError)
        return res.data
    if category is None:
        res.update(code=ResponseCode.InvalidParameter)
        return res.data

    try:
        # set expire time
        flag = Redis.hget(re_phone, 'expire_time')
        if flag is not None:
            flag = datetime.strptime(flag, '%Y-%m-%d %H:%M:%S')
            # throttling
            if (flag - now).total_seconds() < 60:
                res.update(code=ResponseCode.FrequentOperation)
                return res.data

        # get random verification code
        code = "".join([str(random.randint(0, 9)) for _ in range(6)])
        template_param = {"code": code}
        # send verification code
        sms = SendSms(phone=re_phone, category=category,
                      template_param=template_param)
        sms.send_sms()
        # store verification code to redis，for convinence
        Redis.hset(re_phone, "code", code)
        # set expire time
        Redis.hset(re_phone, "expire_time",
                   (now + timedelta(minutes=1)).strftime('%Y-%m-%d %H:%M:%S'))
        # set past time
        Redis.expire(re_phone, 60 * 3)
        return res.data
    except Exception as e:
        logger.exception(e)
        res.update(code=ResponseCode.Fail)
        return res.data


@route(bp, '/testPhoneLoginOrRegister', methods=["POST"])
def test_phone_login_or_register():
    """
    user login or register
    :return:
    """
    res = ResMsg()

    obj = request.get_json(force=True)
    phone = obj.get('account', None)
    code = obj.get('code', None)
    if phone is None or code is None:
        res.update(code=ResponseCode.InvalidParameter)
        return res.data
    # verify the phone code
    flag = PhoneTool.check_phone_code(phone, code)
    if not flag:
        res.update(code=ResponseCode.InvalidOrExpired)
        return res.data

    # login or register
    data = phone_login_or_register(phone)

    if data is None:
        res.update(code=ResponseCode.Fail)
        return res.data
    res.update(data=data)
    return res.data


# --------------------test export PDF-------------------------------#

@route(bp, '/testPDF', methods=["GET"])
def test_pdf():
    """
    test export pdf
    :return:
    """
    res = ResMsg()
    report_path = current_app.config.get("REPORT_PATH", "./report")
    file_name = "{}.pdf".format(uuid.uuid4().hex)
    path = os.path.join(report_path, file_name)
    path = pdf_write(path)
    path = path.lstrip(".")
    res.update(data=path)
    return res.data


# --------------------test Celery-------------------------------#


@route(bp, '/testCeleryAdd', methods=["GET"])
def test_add():
    """
    test add
    :return:
    """
    result = add.delay(1, 2)
    return result.get(timeout=1)


@route(bp, '/testCeleryFlaskAppContext', methods=["GET"])
def test_flask_app_context():
    """
    test flask context
    :return:
    """
    result = flask_app_context.delay()
    return result.get(timeout=1)


