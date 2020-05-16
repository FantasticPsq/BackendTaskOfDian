from wtforms import StringField
from wtforms.validators import Email, InputRequired, Length

from BaseForm import BaseForm
from apps.user.models import User
from apps.libs.exceptions import ParameterException


class LoginForm(BaseForm):
    """
    登陆时验证邮箱和密码
    """
    email = StringField(
        validators=[Email(message="请输入正确的邮箱"), Length(6, 50, message="email"), InputRequired(message="请输入邮箱")])
    password = StringField(validators=[Length(6, 20, message="请正确输入密码(长度范围为6,20"), InputRequired("请输入密码")])


class RegisterForm(BaseForm):
    """
    注册时要验证邮箱、密码、和用户名是否符合要求
    validate_email():验证邮箱是否被注册
    """
    email = StringField(validators=[Length(6, 50), Email(message="请输入正确的邮箱")])
    password = StringField(validators=[Length(6, 20, message="请正确输入密码")])
    username = StringField([InputRequired(message="请输入用户名"), Length(2, 25, message="用户名不得少于2个字符不得多于25个字符")])

    def validate_email(self, email):
        if User.query.filter_by(email=email.data).first():
            raise ParameterException(msg="邮箱已经被注册")
        return True
