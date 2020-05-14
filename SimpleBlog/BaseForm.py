from flask import request, g
from wtforms import Form

from apps.libs.restful import params_error
from werkzeug.datastructures import MultiDict


class BaseForm(Form):
    """
    在Form的基础上添加一些常用功能
    参考https://www.cnblogs.com/zengxm/p/12406499.html
    """

    def __init__(self):
        """
        1.获取请求的JSON数据和查询字符串的内容
        2.将存有JSON数据的data（实际是dict)转成MultiDict,然后传给formdata,为什么？请看super.__init__的源码。
        网上找的资料是直接super.__init__(data=data,**args),但是这种方法在我的电脑上有时可以
        有时又不行，不知道啥问题，于是就改成formdata=MultiDict(data)了，这种方法没有任何异常
        """
        # 获取请求的json数据
        data = request.get_json(silent=True)
        args = request.args.to_dict()
        # 而且在http访问api时，必须加上headers,而且headers中必须要有Content-Type:application/json
        super(BaseForm, self).__init__(formdata=MultiDict(data), **args)

    def validate_for_api(self):
        """
        1.调用父类的validate（）方法看是否有extra的验证(源码中extra保存Form类中的验证,比如validate_id,validate_email等),
        如果有则进行验证，验证成功返回True,验证不成功抛出异常（或者返回False也可以)；如果没有则直接返回True
        :return:
        """
        valid = super(BaseForm, self).validate()
        if not valid:
            return params_error(message=self.errors)
        return self

    # 由于多处需要用到form.errors,所以封装为一个函数
    # 此函数是自己一点一点试出来的
    def get_error(self):
        """
        self.errors经常要用到，get_error只是为了提取我们需要的错误信息
        :return:
        """
        message = self.errors.popitem()[1][0]
        return message
