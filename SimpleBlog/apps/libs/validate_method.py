from flask import request

from apps.libs.exceptions import RequestMethodNotAllowed


def validate_method(method):
    """
    封装验证请求方法的方法，便于直接调用。
    :param method: 要验证的请求方法，比如GET,POST,等
    :return:
    """
    if request.method != method:
        raise RequestMethodNotAllowed(msg="The method %s is not allowed for the requested URL" % request.method)
