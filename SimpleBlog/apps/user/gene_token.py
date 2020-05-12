from flask import current_app
# TimedJSONWebSignatureSerializer参考：http://codingdict.com/sources/py/itsdangerous/13837.html
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


def generate_token(uid, expiration=7200):
    """
    生成存储用户id的token
    :param uid: 用户id
    :param expiration: 过期时间(s)
    :return: 返回序列化后生成的token
    """
    s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
    return s.dumps({'uid': uid})
