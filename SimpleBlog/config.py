# encoding: utf-8
import os
from sqlalchemy import create_engine

# 用于加盐
from exts import db

SECRET_KEY = os.urandom(24)

# 开启Debug模式
DEBUG = True

# 配置数据库相关信息
DB_USERNAME = 'root'
DB_PASSWORD = '1234'
DB_HOST = '127.0.0.1'
DB_PORT = '3306'

DB_NAME = 'simple_blog'
DB_URI = 'mysql+pymysql://%s:%s@%s:%s/%s?charset=utf8' % (DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME)
SQLALCHEMY_BINDS = {
    'usa': 'mysql+pymysql://%s:%s@%s:%s/blog_usa?charset=utf8' % (DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT),
    'china': DB_URI
}
SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False
