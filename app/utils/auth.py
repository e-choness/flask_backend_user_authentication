import jwt
from datetime import datetime, timedelta
from flask import current_app, request, session
from functools import wraps
from app.utils.code import ResponseCode
from app.utils.util import ResMsg


class Auth(object):
    key = 'super-man$&123das%qzq'

    @classmethod
    def generate_access_token(cls, user_id, algorithm: str = 'HS256', exp: float = 2):
        """
        generate access_token
        :param user_id:
        :param algorithm:
        :param exp:
        :return:
        """

        key = current_app.config.get('SECRET_KEY', cls.key)
        now = datetime.now(datetime.timezone.utc)
        exp_datetime = now + timedelta(hours=exp)
        access_payload = {
            'exp': exp_datetime,
            'flag': 0,
            'iat': now,
            'iss': 'qin',
            'user_id': user_id
        }
        access_token = jwt.encode(access_payload, key, algorithm=algorithm)
        return access_token

    @classmethod
    def generate_refresh_token(cls, user_id, algorithm: str = 'HS256', fresh: float = 30):
        """
        generate refresh_token

        :param user_id:
        :param algorithm:
        :param fresh:
        :return:
        """
        key = current_app.config.get('SECRET_KEY', cls.key)

        now = datetime.now(datetime.timezone.utc)
        exp_datetime = now + timedelta(days=fresh)
        refresh_payload = {
            'exp': exp_datetime,
            'flag': 1,
            'iat': now,
            'iss': 'qin',
            'user_id': user_id
        }

        refresh_token = jwt.encode(refresh_payload, key, algorithm=algorithm)
        return refresh_token

    @classmethod
    def encode_auth_token(cls, user_id: str,
                          exp: float = 2,
                          fresh: float = 30,
                          algorithm: str = 'HS256') -> list[str]:
        """
        :param user_id: 
        :param exp: access_token expire time
        :param fresh:  refresh_token expire time
        :param algorithm: encryption algorithm
        :return:
        """
        access_token = cls.generate_access_token(user_id, algorithm, exp)
        refresh_token = cls.generate_refresh_token(user_id, algorithm, fresh)
        return access_token, refresh_token

    @classmethod
    def decode_auth_token(cls, token: str):
        """
        validation token
        :param token:
        :return:
        """
        key = current_app.config.get('SECRET_KEY', cls.key)

        try:
            # payload = jwt.decode(auth_token, config.SECRET_KEY, options={'verify_exp': False})
            payload = jwt.decode(token, key=key, )

        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, jwt.InvalidSignatureError):
            return None
        else:
            return payload

    def identify(self, auth_header):
        """
        user authentication
        :return: list
        """
        if auth_header:
            payload = self.decode_auth_token(auth_header)
            if payload is None:
                return False
            if "user_id" in payload and "flag" in payload:
                if payload["flag"] == 1:
                    return False
                elif payload["flag"] == 0:

                    return payload["user_id"]
                else:
                    return False
            else:
                return False
        else:
            return False


def login_required(f):
    """
    login protection
    :param f:
    :return:
    """

    @wraps(f)
    def wrapper(*args, **kwargs):
        res = ResMsg()
        token = request.headers.get("Authorization", default=None)
        if not token:
            res.update(code=ResponseCode.PleaseSignIn)
            return res.data

        auth = Auth()
        user_name = auth.identify(token)
        if not user_name:
            res.update(code=ResponseCode.PleaseSignIn)
            return res.data

        session["user_name"] = user_name
        return f(*args, **kwargs)

    return wrapper
