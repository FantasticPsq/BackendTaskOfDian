from flask import request
from sqlalchemy.orm import sessionmaker

from exts import db


class DBSession:
    """
    封装动态dbsession
    """

    @staticmethod
    def make_session():
        return sessionmaker(bind=db.get_engine(bind=request.args.get('blog_type').lower()))()
