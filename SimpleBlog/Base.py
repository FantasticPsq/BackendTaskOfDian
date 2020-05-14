from contextlib import contextmanager

from sqlalchemy import inspect, orm

from apps.libs.error_code import NotFound

from flask_sqlalchemy import BaseQuery as _BaseQuery, SQLAlchemy


class BaseQuery(_BaseQuery):
    """
    1. 重写父类Query(object)中filter_by方法添加status参数添加到clause再执行filter方法：
    源码中是这样的：
    clauses = [
            _entity_descriptor(self._joinpoint_zero(), key) == value
            for key, value in kwargs.items()
        ]
        return self.filter(*clauses)
    2. 重写get_or_404和first_or_404将查找出错的结果由abort转为json格式的NotFound
    """

    def filter_by(self, **kwargs):
        if 'status' not in kwargs.keys():
            kwargs['status'] = 1
        return super(BaseQuery, self).filter_by(**kwargs)

    def get_or_404(self, ident, description=None):
        rv = self.get(ident)
        if not rv:
            raise NotFound()
        return rv

    def first_or_404(self, description=None):
        rv = self.first()
        if not rv:
            raise NotFound()
        return rv

    def __call__(self, *args, **kwargs):
        pass


db = SQLAlchemy(query_class=BaseQuery)


class Base(db.Model):
    __abstract__ = True
    status = db.Column(db.SmallInteger, default=1)

    def __getitem__(self, item):
        return getattr(self, item)

    def set_attrs(self, attrs_dict):
        for key, value in attrs_dict.items():
            if hasattr(self, key) and key != 'id':
                setattr(self, key, value)

    def delete(self):
        self.status = 0

    def keys(self):
        return self.fields

    def hide(self, *keys):
        for key in keys:
            self.fields.remove(key)
        return self

    def append(self, *keys):
        for key in keys:
            self.fields.append(key)
        return self
