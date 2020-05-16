from flask import Blueprint

from .gene_token import generate_token
from .forms import RegisterForm, LoginForm
from .models import User
from apps.libs.exceptions import ParameterException, AuthFailed, Success
from config import ALL_METHODS

from ..libs.dbsession import DBSession
from ..libs.validate_method import validate_method

# 用户蓝图，访问需加前缀/user
from ..libs.verify_token import verify

bp = Blueprint('user', __name__, url_prefix='/user')


@bp.before_request
def before_request():
    global dbsession
    dbsession = DBSession.make_session()


@bp.route('/login/', methods=ALL_METHODS)
def login():
    """
    验证Request method是否为POST,如果不是抛出405 method not allowed
    登录接口：验证提交的数据是否为JSON数据并且进行表单验证
    验证通过后产生token,返回success，否则返回参数错误
    :return:
    """
    validate_method("POST")
    form = LoginForm()
    if form.validate_for_api() and form.validate():
        user = dbsession.query(User).filter_by(email=form.email.data).first()
        if not (user and user.check_password(form.password.data)):
            return AuthFailed(msg="用户名或密码错误")
        # token默认过期时间为2小时
        token = generate_token(user.id)
        t = {
            'token': token.decode('ascii')
        }
        return Success(data=t, msg="登录成功", code=201)
    return AuthFailed(msg=form.get_errors())


@bp.route('/register/', methods=ALL_METHODS)
def register():
    """
    验证Request method是否为POST,如果不是抛出405 method not allowed
    注册接口：进行JSON数据格式验证并且进行表单验证
    验证通过向数据库中插入新的用户数据，返回success,
    否则返回参数错误
    :return:
    """
    validate_method("POST")
    form = RegisterForm()
    if form.validate_for_api() and form.validate():
        if form.validate_email(form.email):
            email = form.email.data
            password = form.password.data
            username = form.username.data
            user = User(email=email, username=username, password=password)
            dbsession.add(user)
            dbsession.commit()
            return Success(msg="注册成功")
    return ParameterException(msg=form.get_errors(), code=201)
