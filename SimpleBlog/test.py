from flask import Flask

import datetime
from sqlalchemy import Column, String, create_engine, DateTime, func
from config import engine

app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base, DeferredReflection
from sqlalchemy.orm import sessionmaker, scoped_session

# Base = declarative_base(cls=DeferredReflection)
Base = declarative_base()


class testuser(Base):
    __tablename__ = 'testuser'
    # 当前数据库名字是 test
    __table_args__ = {'schema': 'test'}

    id = Column(String(20), primary_key=True)
    name = Column(String(20))
    woncreated = Column(DateTime, default=datetime.datetime.utcnow())
    wontimestamp = Column(DateTime, default=datetime.datetime.utcnow(), onupdate=datetime.datetime.utcnow())


#
class testuser2(Base):
    __tablename__ = 'testuser2'

    # 关联查询的另一个数据库是 test2
    __table_args__ = {'schema': 'test2'}

    id = Column(String(20), primary_key=True)
    name = Column(String(20))
    woncreated = Column(DateTime, default=datetime.datetime.utcnow())
    wontimestamp = Column(DateTime, default=datetime.datetime.utcnow(), onupdate=datetime.datetime.utcnow())


# Base.prepare(engine)
dbsession = scoped_session(sessionmaker(
    autocommit=False, autoflush=False, bind=engine))


@app.route('/')
def index():
    import pdb
    pdb.set_trace()
    qq = dbsession.query(testuser).join(testuser2,
                                        testuser.id == testuser2.id).all()
    return str(tuple(q.__dict__ for q in qq))


if __name__ == '__main__':
    app.run()
