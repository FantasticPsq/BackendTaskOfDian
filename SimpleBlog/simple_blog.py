"""
Created by 彭少青 on 2010/5/9 .
本app无论请求还是结果都是Json形式，目的是尽量满足restful要求
"""
from datetime import date

from flask import Flask as _Flask
import config
from apps.libs.error_code import ServerError
from apps.user.views import bp
from apps.article.views import bp as article_bp
from exts import db
from flask.json import JSONEncoder as _JSONEncoder
# 只有导入模型，模型才能迁移至数据库
import apps.user.models


class JSONEncoder(_JSONEncoder):
    """
    配置JSON的编码器
    参考flask中文文档：https://dormousehole.readthedocs.io/en/latest/api.html#module-flask.json
    """

    def default(self, o):
        """
        在子类中实现此方法，以使其返回可序列化的对象o
        :param o: 可序列化的对象
        :return: 返回可序列化的对象o
        如果既不是date实例也没有keys和__getitem__属性，则抛出500错误
        """
        if hasattr(0, 'keys') and hasattr(o, '__getitem__'):
            return dict(o)
        # 时间类型是不能被序列化的
        if isinstance(o, date):
            return o.strftime('%Y-%m-%d')
        raise ServerError()


# 更改Flask中的默认json_encoder
class Flask(_Flask):
    """
    将默认编码器改为自定义的JSONEncoder
    """
    json_encoder = JSONEncoder


def create_app():
    """
    产生app的工厂方法
    初始化app,配置，绑定数据库，以及注册蓝图等
    :return:
    """
    app = Flask(__name__)

    app.register_blueprint(bp)
    app.register_blueprint(article_bp)
    app.config.from_object(config)
    # 数据库初始化app(相当于绑定数据库和app)
    db.init_app(app)
    return app


if __name__ == '__main__':
    app_ = create_app()
    # 运行在8080端口
    app_.run(port=8080)
