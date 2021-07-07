import json
from urllib import parse, request
from flask import current_app
from app.models.model import UserLoginMethod, User
from app.utils.core import db


def get_access_code(code: str, flag: str):
    """
    :param code
    :param flag
    :return
    """
    if flag == "web":
        app_id = current_app.config.get("WEB_ID")
        secret = current_app.config.get("WEB_SECRET")
    elif flag == "app":
        app_id = current_app.config.get("APP_ID")
        secret = current_app.config.get("APP_SECRET")
    else:
        return None
    try:
        fields = parse.urlencode(
            {"appid": app_id, "secret": secret,
             "code": code, "grant_type": "authorization_code"}
        )
        url = 'https://api.weixin.qq.com/sns/oauth2/access_token?{}'.format(fields)
        print(url)
        req = request.Request(url=url, method="GET")
        res = request.urlopen(req, timeout=10)
        access_data = json.loads(res.read().decode())
        print(access_data)
    except Exception as e:
        print(e)
        return None

    # {
    # "access_token": "ACCESS_TOKEN", "expires_in": 7200,"refresh_token": "REFRESH_TOKEN",
    # "openid": "OPENID","scope": "SCOPE"
    # }

    if "openid" in access_data:
        return access_data

    # {
    # "errcode":40029,"errmsg":"invalid code"
    # }
    else:
        return None


def get_wx_user_info(access_data: dict):
    """
    :return:
    """
    openid = access_data.get("openid")
    access_token = access_data.get("access_token")
    try:
        fields = parse.urlencode({"access_token": access_token, "openid": openid})
        url = 'https://api.weixin.qq.com/sns/userinfo?{}'.format(fields)
        print(url)
        req = request.Request(url=url, method="GET")
        res = request.urlopen(req, timeout=10)
        wx_user_info = json.loads(res.read().decode())
        print(wx_user_info)
    except Exception as e:
        print(e)
        return None

    # {
    # "openid":"OPENID",
    # "nickname":"NICKNAME",
    # "sex":1,
    # "province":"PROVINCE",
    # "city":"CITY",
    # "country":"COUNTRY",
    # "headimgurl": "test.png",
    # "privilege":[
    # "PRIVILEGE1",
    # "PRIVILEGE2"
    # ],
    # "unionid": " o6_bmasdasdsad6_2sgVt7hMZOPfL"
    #
    # }
    if "openid" in wx_user_info:
        return wx_user_info
    # {"errcode":40003,"errmsg":"invalid openid"}
    else:
        return None


def wx_login_or_register(wx_user_info):
    """
    :param wx_user_info
    :return:
    """
    unionid = wx_user_info.get("unionid")
    nickname = wx_user_info.get("nickname")
    if unionid is None:
        return None

    user_login = db.session(UserLoginMethod). \
        filter(UserLoginMethod.login_method == "WX",
               UserLoginMethod.identification == unionid, ).first()
    if user_login:
        user = db.session.query(User.id, User.name).filter(User.id == user_login.user_id).first()
        data = dict(zip(user.keys(), user))
        return data
    else:
        try:
            new_user = User(name=nickname, age=20)
            db.session.add(new_user)
            db.session.flush()
            new_user_login = UserLoginMethod(user_id=new_user.id,
                                             login_method="WX",
                                             identification=unionid,
                                             access_code=None)
            db.session.add(new_user_login)
            db.session.flush()
            db.session.commit()
        except Exception as e:
            print(e)
            return None

        data = dict(id=new_user.id, name=User.name)
        return data
