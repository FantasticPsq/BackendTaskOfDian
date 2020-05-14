"""
 定义几个常用的HTTP类
"""

from apps.libs.error import APIException

__author__ = '七月'


class Success(APIException):
    code = 201
    msg = 'ok'


class DeleteSuccess(Success):
    code = 202


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
