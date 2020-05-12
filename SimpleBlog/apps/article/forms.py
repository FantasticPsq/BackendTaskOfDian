from BaseForm import BaseForm
from wtforms.validators import Email, InputRequired, Length
from wtforms import StringField, IntegerField
from flask import g

from apps.libs.dbsession import DBSession
from apps.user.models import Article, User
from apps.libs.error_code import NotFound, AuthFailed


class ArticlePublishForm(BaseForm):
    title = StringField(validators=[InputRequired(message="请输入文章标题")])
    content = StringField()


class ArticleModifyForm(BaseForm):
    id = IntegerField()
    title = StringField(validators=[InputRequired(message="请输入标题")])
    content = StringField()

    @staticmethod
    def validate_id(self, id_):
        """
        由于id可能在数据库中不存在或者该article对应的作者不是该作者，所以需要验证id是否在数据库中存在
        以及该作者是否能修改该文章（作者不能随意修改别人的文章)
        先用Article查询所有的articles，判断id_是否在这些id中，不在抛出404 notfound
        再用User查询当前登录的用户,通过一对多关系直接找出所有articles，再判断id_是否在这些id中
        不在则抛出401 AuthFailed
        定义其为staticmothod是为了让ArticleDeleteForm方便使用
        :param self:
        :param id_: <input id="id" name="id" type="text" value="4">
        :return:
        """
        dbsesson = DBSession.make_session()
        user = dbsesson.query(User).filter_by(id=g.user.uid).first()
        id_s1 = []
        id_s2 = []
        for article in user.articles:
            id_s1.append(article.id)
        articles = dbsesson.query(Article).filter(Article.id).all()
        for article in articles:
            id_s2.append(article.id)
        if id_.data not in id_s2:
            raise NotFound(msg="找不到您要修改的文章")
        if id_.data not in id_s1:
            raise AuthFailed(msg="您没有修改该文章的权限")


class ArticleDeleteForm(BaseForm):
    id = IntegerField()

    # 验证id是否合法
    def validate_id(self, id_):
        ArticleModifyForm.validate_id(self, id_)
