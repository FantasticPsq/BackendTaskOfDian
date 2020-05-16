from flask import request, redirect, url_for

from flask import Blueprint, g

from flask_paginate import get_page_parameter
from sqlalchemy import or_

import config
from apps.libs.verify_token import auth
from config import ALL_METHODS
from .forms import ArticlePublishForm, ArticleModifyForm
from ..libs.exceptions import ParameterException, Success, DeleteSuccess
from ..user.models import Article
from apps.libs.dbsession import DBSession
from ..libs.validate_method import validate_method
from ..libs.query_string import get_query_string

# article蓝图实现与article有关的路由,前缀为article
bp = Blueprint('article', __name__, url_prefix='/article')


@bp.before_request
def before_request():
    """
    使用before_request钩子进行全局实例化Session。供所有视图函数使用。
    从而不必在每个视图函数中去实例化。
    :return:
    """
    global dbsession
    dbsession = DBSession.make_session()


@bp.route('/publish/', methods=ALL_METHODS)
@auth.login_required
def publish():
    """
    1.验证token信息和request method
    2.进行JSON数据格式和表单验证，验证成功后通过g.user获取用户uid,然后像数据库插入数据，
    返回success,否则返回参数错误
    :return: Success 201 or Bad Request 400
    """
    validate_method('POST')
    form = ArticlePublishForm()
    if form.validate_for_api() and form.validate():
        title = form.title.data
        content = form.content.data
        uid = g.user.uid
        article = Article(title=title, content=content, uid=uid)
        dbsession.add(article)
        dbsession.commit()
        return Success(msg="发布文章成功", data={"article_published": article.title}, code=201)
    else:
        return ParameterException(msg=form.get_errors())


@bp.route('/modify/', methods=ALL_METHODS)
@auth.login_required
def modify():
    """
    1.验证token信息和request method
    2.JSON数据格式验证和表单验证，通过传进来的article_id查询原先的article,然后更改article信息
    :return: success 201 or ParameterException 400 or notfound 404
    """
    validate_method("PUT")
    form = ArticleModifyForm()
    if form.validate_for_api() and form.validate():
        article_id = form.id.data
        title = form.title.data
        content = form.content.data
        article = dbsession.query(Article).filter_by(id=article_id).first_or_404(description="文章不存在或者已被删除")
        article.title = title
        article.content = content
        dbsession.commit()
        return Success(msg="修改文章成功", data={"article_modified": article.title}, code=201)
    else:
        return ParameterException(msg=form.get_errors())


@bp.route("/delete/<int:id_>", methods=ALL_METHODS)
@auth.login_required
def delete(id_):
    """
    实现数据伪删除，也可以通过传入delete_mode='forever'以永久删除。
    1.验证token和请求的method
    2.通过id_查询数据库,使用get_or_404来查找status=1的结果，否则抛出404 notfound
    :return: success 202 or notfound 400
    """
    validate_method('DELETE')
    article = dbsession.query(Article).get_or_404(id_)
    if article.status == 1:
        if (request.args.get("delete_mode") and request.args.get(
                "delete_mode").lower() == "forever") or config.DELETE_FOREVER:
            dbsession.delete()
        else:
            article.delete()
        dbsession.commit()
        return DeleteSuccess(msg="删除文章成功",
                             data={
                                 "article_deleted": {"article_title": article.title,
                                                     "article_content": article.content}})
    return ParameterException(msg="您要找的文章已被删除，请勿重复删除")


@bp.route('/list_all/', methods=ALL_METHODS)
@auth.login_required
def list_all():
    """
    1.验证token和GET方法
    2.从数据库中把所有的数据查出来，然后保存在article_titles中，以标题代表文章
    查询的数据分页展示
    :return: success 200
    """
    validate_method("GET")
    # 获取输入的page,默认为1,关键字默认为page,get_page_parameter()自动获取page
    page = request.args.get(get_page_parameter(), default=1, type=int)
    # 计算起始页和结束页
    start = (page - 1) * config.PER_PAGE
    end = start + config.PER_PAGE
    article_titles = []
    articles = dbsession.query(Article).slice(start, end)
    if articles:
        for article in articles:
            if article.status == 1:
                article_titles.append(article.title)
    return Success(data={"articles_in_page_%s" % page: article_titles}, msg="获取文章列表成功")


@bp.route('/details/<int:id_>', methods=ALL_METHODS)
@auth.login_required
def details(id_):
    """
    1.验证GET方法
    2.通过first_or_404验证id_
    :param id_: 文章的id
    :return: success 200
    """
    validate_method("GET")
    article = dbsession.query(Article).filter_by(id=id_).first_or_404(description="文章不存在或者已被删除")
    title = article.title
    content = article.content
    return Success(msg="这是文章详情页", data={'文章标题': title, '文章内容': content})


@bp.route('/search/', methods=ALL_METHODS)
@auth.login_required
def query():
    """
    1.验证token和request method
    2，如果没有传进来kw,则获取查询字符串query_string重定向到list_all默认分页显示所有文章
    3.如果有kw，则查询显示所有文章（可通过title和content进行匹配)
    :return: success 200
    """
    validate_method("GET")
    kw = request.args.get("kw")
    if not kw:
        return redirect(url_for('article.list_all') + get_query_string())
    query_kw = "%" + kw + "%"
    content = dbsession.query(Article.title, Article.content).filter(
        or_(Article.title.like(query_kw), Article.content.like(query_kw))).all()
    return Success(msg="以上是为您搜索到的信息", data={"search_results": content})
