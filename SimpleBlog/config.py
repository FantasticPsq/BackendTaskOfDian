# encoding: utf-8
import os

# 用于加盐
SECRET_KEY = os.urandom(24)

# 开启Debug模式
DEBUG = True

# 配置数据库相关信息
DB_USERNAME = 'root'
DB_PASSWORD = '1234'
DB_HOST = '127.0.0.1'
DB_PORT = '3306'

# 配置默认数据库
DB_NAME = 'blog_china'
DB_URI = 'mysql+pymysql://%s:%s@%s:%s/%s?charset=UTF8MB4' % (DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME)

# SQLALCHEMY_BINDS用于数据库动态绑定,可以通过添加key,value来实现数据库的拓展
SQLALCHEMY_BINDS = {
    'usa': 'mysql+pymysql://%s:%s@%s:%s/blog_usa?charset=UTF8MB4' % (DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT),
    'china': DB_URI
}
SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False

# 请求方法设置，用于验证请求方法。
ALL_METHODS = ['GET', 'POST', 'PUT', "DELETE", "HEAD"]

# flask_paginate分页设置，设置每页展示的文章个数
PER_PAGE = 3

# 配置删除模式，一旦开启不管前端传不传delete_mode都将是永远删除。
DELETE_FOREVER = False


