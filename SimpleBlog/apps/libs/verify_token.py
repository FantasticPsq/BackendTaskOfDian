from collections import namedtuple

from flask import current_app, g
from flask_httpauth import HTTPTokenAuth
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired

from apps.libs.exceptions import AuthFailed

# 使用HTTPTokenAuth进行token验证，定义scheme为JWT
auth = HTTPTokenAuth(scheme="JWT")
# 定义namedtuple就不用在user模型中重写keys方法了
# 可以通过属性的方式获取uid
User = namedtuple('User', ['uid'])


@auth.verify_token
def verify(token):
    """
    通过反序列化loads验证token是否有效,需确保有SECRET_KEY加盐
    :param token: 用户在Authorization中传递过来的token值
    :return: 如果有效返回True,无效则根据对应异常抛出错误401(注意这里不能简单return params_error())
    """
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
    except BadSignature:
        raise AuthFailed(msg="token is invalid")
    except SignatureExpired:
        raise AuthFailed(msg="token is expired")
    # 反序列化出来后，获取用户id,并将用户id绑定到g.user,g.user也就是一个namedtuple实例
    # flask是线程隔离的，多个用户的g.user互不影响
    uid = data['uid']
    user = User(uid)
    g.user = user
    return True
