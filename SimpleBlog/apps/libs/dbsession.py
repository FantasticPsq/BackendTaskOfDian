from flask import request
from sqlalchemy.orm import sessionmaker

from exts import db


class DBSession:
    """
    封装动态dbsession
    """

    @staticmethod
    def make_session():
        # 由于调用了lower()方法所以要判断是否传了blog_type
        if request.args.get('blog_type'):
            return sessionmaker(bind=db.get_engine(bind=request.args.get('blog_type').lower()))()
        else:
            return sessionmaker(bind=db.get_engine())()
