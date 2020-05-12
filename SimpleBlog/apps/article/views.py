from flask import Blueprint, g, request
from sqlalchemy.orm import sessionmaker

from apps.user.verify_token import auth
from .forms import ArticlePublishForm, ArticleModifyForm, ArticleDeleteForm
from ..libs.error_code import NotFound
from ..libs.restful import params_error, success
from ..user.models import Article, User
from exts import db
from apps.libs.dbsession import DBSession

bp = Blueprint('article', __name__, url_prefix='/article')


@bp.route('/publish/', methods=['POST'])
@auth.login_required
def publish():
    """
    1.验证POST方法，验证token信息
    2.进行JSON数据格式和表单验证，验证成功后通过g.user获取用户uid,然后像数据库插入数据，
    返回success,否则返回参数错误
    :return: success or params_error
    """
    dbsession = DBSession.make_session()
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
@bp.route('/modify/', methods=["PUT"])
@auth.login_required
def modify():
    """
    1.验证请求方法是否为PUT,再验证token信息
    2.JSON数据格式验证和表单验证，通过传进来的article_id查询原先的article,然后更改article信息
    :return: success 200 or params_error 400 or notfound 404
    """
    dbsession = DBSession.make_session()
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


@bp.route("/delete/", methods=['DELETE'])
@auth.login_required
def delete():
    """
    首先实现数据库层面的删除，有时间再优化

    1.验证请求方法是否为DELETE,再验证token
    2.验证JSON数据格式和表单，通过传进来的article_id查询并删除article
    :return: success 200 or params_error 400
    """
    dbsession = DBSession.make_session()
    form = ArticleDeleteForm()
    if form.validate_for_api and form.validate():
        article_id = form.id.data
        article = dbsession.query(Article).filter_by(id=article_id).first()
        dbsession.delete(article)
        dbsession.commit()
        return success(message="删除文章成功")
    else:
        return params_error(message=form.get_error())


@bp.route('/list_all/', methods=['GET'])
def list_all():
    """
    1.验证GET方法
    2.从数据库中把所有的数据查出来，然后保存在article_titles中，以标题代表文章
    :return: success 200
    """
    dbsession = DBSession.make_session()
    article_titles = []
    articles = dbsession.query(Article).filter(Article.id).all()
    if articles:
        for article in articles:
            article_titles.append(article.title)
    return success(data={"all_articles": article_titles}, message="获取文章列表成功")


@bp.route('/details/<int:id_>', methods=['GET'])
def details(id_):
    """
    1.验证GET方法
    :param id_: 文章的id
    :return: success 200
    """
    dbsession = DBSession.make_session()
    article = dbsession.query(Article).filter_by(id=id_).first()
    if article:
        title = article.title
        content = article.content
        return success(message="这是文章详情页", data={'文章标题': title, '文章内容': content})
    else:
        raise NotFound(msg='没有找到您要查看的文章')
