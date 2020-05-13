from flask import Blueprint, request

from .gene_token import generate_token
from .forms import RegisterForm, LoginForm
from .models import User
from apps.libs.restful import unauthorized_error, params_error, success
from apps.libs.error_code import RequestMethodNotAllowed
from config import ALL_METHODS

# 用户蓝图，访问需加前缀/user
from ..libs.dbsession import DBSession

bp = Blueprint('user', __name__, url_prefix='/user')


@bp.route('/login/', methods=ALL_METHODS)
def login():
    """
    验证Request method是否为POST,如果不是抛出405 method not allowed
    登录接口：验证提交的数据是否为JSON数据并且进行表单验证
    验证通过后产生token,返回success，否则返回参数错误
    :return:
    """
    print(request.method)
    if request.method != 'POST':
        raise RequestMethodNotAllowed(msg="The method %s is not allowed for the requested URL" % request.method)
    dbsession = DBSession.make_session()
    form = LoginForm()
    if request.method == 'POST' and form.validate_for_api() and form.validate():
        user = dbsession.query(User).filter_by(email=form.email.data).first()
        if not user:
            return unauthorized_error(message="邮箱错误")
        if not user.check_password(form.password.data):
            return unauthorized_error(message="密码错误")
        # token默认过期时间为2小时
        token = generate_token(user.id)
        t = {
            'token': token.decode('ascii')
        }
        return success(data=t, message="登录成功")
    return params_error(message=form.get_error())


@bp.route('/register/', methods=ALL_METHODS)
def register():
    """
    验证Request method是否为POST,如果不是抛出405 method not allowed
    注册接口：进行JSON数据格式验证并且进行表单验证
    验证通过向数据库中插入新的用户数据，返回success,
    否则返回参数错误
    :return:
    """
    print(request.method)
    if request.method.upper() != 'POST':
        raise RequestMethodNotAllowed(msg="The method %s is not allowed for the requested URL" % request.method)
    dbsession = DBSession.make_session()
    form = RegisterForm()
    if form.validate_for_api() and form.validate():
        if form.validate_email(form.email):
            email = form.email.data
            password = form.password.data
            username = form.username.data
            user = User(email=email, username=username, password=password)
            dbsession.add(user)
            dbsession.commit()
            return success(message="注册成功")
    return params_error(message=form.get_error())
