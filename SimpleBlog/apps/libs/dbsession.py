from flask import request
from sqlalchemy.orm import Session

from Base import BaseQuery
from exts import db


class DBSession:
    """
    封装动态dbsession，将sessionmaker类的bind根据db.get_engine(bind=blog_type)重置
    实现数据库的动态链接
    思路来自sessionmaker的configure方法源码
    后来由于makesession和BaseQuery(Base中的BaseQuery)无法绑定，就改为使用Session了。Session的query_cls可以和BaseQuery进行绑定
    """

    @staticmethod
    def make_session():
        # 由于调用了lower()方法所以要判断是否传了blog_type
        if request.args.get('blog_type'):
            return Session(bind=db.get_engine(bind=request.args.get('blog_type').lower()), query_cls=BaseQuery)
        else:
            return Session(bind=db.get_engine(), query_cls=BaseQuery)
