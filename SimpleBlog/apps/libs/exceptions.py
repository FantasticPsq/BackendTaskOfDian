"""
 定义几个常用的HTTP类
"""

from apps.libs.api_exception import APIException


class Success(APIException):
    """
    code=200通常表示请求成功服务器返回所需数据
    code=201通常表示服务器执行成功，创建/某种新的东西或者删除原有东习。
    """
    code = 200
    msg = 'ok'


class DeleteSuccess(Success):
    code = 201
    msg = "服务器执行成功"


class ServerError(APIException):
    code = 500
    msg = 'sorry, we made a mistake (*￣︶￣)!'


class ParameterException(APIException):
    code = 400
    msg = 'invalid parameter'


class NotFound(APIException):
    code = 404
    msg = 'the resource are not found O__O...'


class AuthFailed(APIException):
    code = 401
    msg = 'authorization failed'


class RequestMethodNotAllowed(APIException):
    code = 405
    msg = "The method is not allowed for the requested URL"
