from flask import request

from flask import Blueprint, g

from flask_paginate import get_page_parameter

import config
from Base import db
from apps.user.verify_token import auth
from config import ALL_METHODS
from .forms import ArticlePublishForm, ArticleModifyForm, ArticleDeleteForm
from ..libs.error_code import NotFound, RequestMethodNotAllowed
from ..libs.restful import params_error, success
from ..user.models import Article
from apps.libs.dbsession import DBSession

bp = Blueprint('article', __name__, url_prefix='/article')


@bp.before_request
def before_request():
    global dbsession
    dbsession = DBSession.make_session()


@bp.route('/publish/', methods=ALL_METHODS)
@auth.login_required
def publish():
    """
    1.验证POST方法，验证token信息
    2.进行JSON数据格式和表单验证，验证成功后通过g.user获取用户uid,然后像数据库插入数据，
    返回success,否则返回参数错误
    :return: success or params_error
    """
    if request.method != 'POST':
        raise RequestMethodNotAllowed(msg="The method %s is not allowed for the requested URL" % request.method)
    form = ArticlePublishForm()
    if form.validate_for_api() and form.validate():
        title = form.title.data
        content = form.content.data
        uid = g.user.uid
        article = Article(title=title, content=content, uid=uid)
        dbsession.add(article)
        dbsession.commit()
        return success(message="发布文章成功")
    else:
        return params_error(message=form.get_error())


# 修改指定为put方法
@bp.route('/modify/', methods=ALL_METHODS)
@auth.login_required
def modify():
    """
    1.验证请求方法是否为PUT,再验证token信息
    2.JSON数据格式验证和表单验证，通过传进来的article_id查询原先的article,然后更改article信息
    :return: success 200 or params_error 400 or notfound 404
    """
    if request.method != 'PUT':
        raise RequestMethodNotAllowed(msg="The method %s is not allowed for the requested URL" % request.method)
    form = ArticleModifyForm()
    if form.validate_for_api() and form.validate():
        article_id = form.id.data
        title = form.title.data
        content = form.content.data
        article = dbsession.query(Article).filter_by(id=article_id).first()
        if article:
            article.title = title
            article.content = content
            dbsession.commit()
            return success(message="修改文章成功")
    else:
        return params_error(message=form.get_error())


@bp.route("/delete/", methods=ALL_METHODS)
@auth.login_required
def delete():
    """
    首先实现数据库层面的删除，有时间再优化
    1.验证请求方法是否为DELETE,再验证token
    2.验证JSON数据格式和表单，通过传进来的article_id查询并删除article
    :return: success 200 or params_error 400
    """
    if request.method != 'DELETE':
        raise RequestMethodNotAllowed(msg="The method %s is not allowed for the requested URL" % request.method)
    form = ArticleDeleteForm()
    if form.validate_for_api and form.validate():
        article_id = form.id.data
        article = dbsession.query(Article).get_or_404(article_id)
        article.delete()
        dbsession.commit()
        return success(message="删除文章成功",
                       data={"article_deleted": {"article_title": article.title, "article_content": article.content}})
    else:
        return params_error(message=form.get_error())


@bp.route('/list_all/', methods=ALL_METHODS)
@auth.login_required
def list_all():
    """
    1.验证GET方法
    2.从数据库中把所有的数据查出来，然后保存在article_titles中，以标题代表文章
    查询的数据分页展示
    :return: success 200
    """

    if request.method != 'GET':
        raise RequestMethodNotAllowed(msg="The method %s is not allowed for the requested URL" % request.method)
    # 获取输入的page,默认为1
    page = request.args.get(get_page_parameter(), default=1, type=int)
    # 计算起始页和结束页
    start = (page - 1) * config.PER_PAGE
    end = start + config.PER_PAGE
    article_titles = []
    articles = dbsession.query(Article).slice(start, end)
    if articles:
        for article in articles:
            article_titles.append(article.title)
    return success(data={"第%d页的文章" % page: article_titles}, message="获取文章列表成功")


@bp.route('/details/<int:id_>', methods=ALL_METHODS)
@auth.login_required
def details(id_):
    """
    1.验证GET方法
    :param id_: 文章的id
    :return: success 200
    """
    if request.method != 'GET':
        raise RequestMethodNotAllowed(msg="The method %s is not allowed for the requested URL" % request.method)
    article = dbsession.query(Article).filter_by(id=id_).first_or_404()
    if article:
        title = article.title
        content = article.content
        return success(message="这是文章详情页", data={'文章标题': title, '文章内容': content})
    else:
        raise NotFound(msg='没有找到您要查看的文章')

# @bp.route('/search/', methods=ALL_METHODS)
# def query():
#     if request.method != 'GET':
#         raise RequestMethodNotAllowed(msg="The method %s is not allowed for the requested URL" % request.method)
#     kw = request.args.get("kw")
#     if not kw:
#         return redirect(url_for('article.list_all') + "?blog_type=%s" % request.args.get("blog_type"))
#     print(kw)
#     content = dbsession.query(Article.title).filter(
#         Article.title.like('%篇%')).all()
#     print(content)
#     return success(message="以上是为您搜索到的信息", data={"匹配的结果": content})
