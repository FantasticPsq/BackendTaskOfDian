from sqlalchemy.orm import relationship
from exts import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

bind_key = None


# Article模型
class Article(db.Model):
    """
    表名article
    id:主键
    title:文章标题
    content:文章内容
    create_time:文章创建的时间
    uid:意思为user_id,外键，与user关联
    author:建立多对一关系，方便直接从文章获取作者信息
    """
    __tablename__ = 'article'
    __bind_key__ = bind_key
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    # 建立外键关联
    uid = db.Column(db.Integer, db.ForeignKey("user.id"))
    # 由于User和Article属于一堆多的关系，可通过relationship建立关系
    # 其中关键字backref（反向引用）是为了方便User查找他的文章
    author = relationship("User", backref="articles")


class User(db.Model):
    """
    表名user
    id:主键
    username:用户名
    _password:password为隐私字段，不能让外部访问，而且要加密,加密后password会变长，所以String最大长度为100（如果较小的话，可能会被数据库截断）
    email:邮箱
    join_time:用户注册时间
    """
    __bind_key__ = bind_key
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False)
    _password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(25), nullable=False)
    join_time = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email

    @property
    def password(self):
        return self._password

    # set装饰器进行加密
    @password.setter
    def password(self, raw_password):
        self._password = generate_password_hash(raw_password)

    # 验证密码
    def check_password(self, raw_password):
        result = check_password_hash(self.password, raw_password)
        return result
