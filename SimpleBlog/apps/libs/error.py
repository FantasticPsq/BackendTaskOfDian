"""
error.py和error_code.py参考https://github.com/zhangnian/fastapi/tree/master/fastapi/utils
本文件是从上面copy下来的，并稍作修改去掉error_code等
"""
from flask import request, json
from werkzeug.exceptions import HTTPException


class APIException(HTTPException):
    """
    code:错误码
    msg:错误信息
    需要重写get_body方法以返回JSON数据，而不是表单数据。
    需要重写get_header方法设置头部ContentType为application/json
    """
    code = 500
    msg = "Sorry, Some mistakes occurred"

    def __init__(self, msg=None, code=None, data=None):
        if msg:
            self.msg = msg
        if code:
            self.code = code
        if data:
            self.data = data
        super(APIException, self).__init__(msg, None)

    def get_body(self, environ=None):
        body = dict(
            msg=self.msg,
            code=self.code,
            # request=request.method + " " + self.get_url_no_param()
        )
        text = json.dumps(body)
        return text

    def get_headers(self, environ=None):
        return [('Content-Type', 'application/json')]

    # @staticmethod
    # def get_url_no_param():
    #     full_path = request.full_path
    #     main_path = full_path.split('?')
    #     return main_path[0]
