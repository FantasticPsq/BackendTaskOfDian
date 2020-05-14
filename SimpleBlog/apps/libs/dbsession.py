from contextlib import contextmanager

from flask import request
from sqlalchemy.orm import sessionmaker

from exts import db


class DBSession:
    """
    封装动态dbsession，将sessionmaker类的bind根据db.get_engine(bind=blog_type)重置
    实现数据库的动态链接
    思路来自sessionmaker的configure源码
    """

    def __init__(self):
        self.dbsession = self.make_session()

    @staticmethod
    def make_session():
        # 由于调用了lower()方法所以要判断是否传了blog_type
        if request.args.get('blog_type'):
            return sessionmaker(bind=db.get_engine(bind=request.args.get('blog_type').lower()))()
        else:
            return sessionmaker(bind=db.get_engine())()

    @contextmanager
    def auto_commit(self):
        try:
            yield
            self.dbsession.commit()
        except Exception as e:
            self.dbsession.rollback()
            raise e
