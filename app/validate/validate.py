from wtforms import PasswordField, StringField, IntegerField, FieldList
from wtforms.validators import DataRequired, EqualTo, Regexp, Email, Length, AnyOf, Optional
from app.exception import ParameterException
from app.utils import time2stamp
from .base import JsonValidate


class LoginValidate(JsonValidate):
    password = PasswordField('密码', validators=[
        DataRequired(message="密码不可为空"),
        Regexp(r'^^[a-zA-Z0-9!@#$%^&*()_+]{6,20}$',
               message='用户名或密码错误'),
    ])
    username = StringField('用户名', validators=[
        Length(min=0, max=128, message="用户名或密码错误"),
    ])
    email = StringField('邮件', validators=[
        Email(message='请输入有效的邮箱地址，比如：username@domain.com'),
        Optional()
    ])

    def validate_username(self, value):
        if not (value.data or self.email.data):
            raise ParameterException("请输入用户名或邮箱")
        setattr(self, 'login', {'username': value.data} if value.data else {'email': self.email.data})


class RegisterValidate(JsonValidate):
    username = StringField('用户名', validators=[
        DataRequired(message='用户名不能为空'),
        Length(min=0, max=128, message="用户名长度在0-128字符间")
    ])
    nickname = StringField('昵称', validators=[
        DataRequired(message='昵称不能为空'),
        Length(min=0, max=128, message="昵称长度在0-128字符间")
    ])

    password = PasswordField('密码', validators=[
        DataRequired(message='密码不可为空'),
        Regexp(r'^[a-zA-Z0-9!@#$%^&*()_+]{6,20}$',
               message='密码长度为6-20个字符,可以为字母,数字,!@#$%^&*()_+'),
        EqualTo('confirm_password', message='两次输入密码不一致')
    ])
    confirm_password = PasswordField('确认密码', validators=[
        DataRequired(message='请确认密码')
    ])
    email = StringField('邮件', validators=[
        Email(message='请输入有效的邮箱地址，比如：username@domain.com'),
        Optional()
    ])


class PostValidate(JsonValidate):
    id = IntegerField('文章id', validators=[
        DataRequired(message='id不能为空'),
    ])
    title = StringField('文章标题', validators=[
        Length(0, 128, message="文章标题在0~128字符之间")
    ])
    tags = FieldList(StringField('标签'), min_entries=0)
    visibility = StringField('文章可见性', validators=[
        DataRequired(message='visibility不能为空'),
        AnyOf(['私密', '公开'], message="visibility只能为私密或公开")
    ])
    change_date = IntegerField('文章修改日期', validators=[
        DataRequired(message='change_date不能为空'),
    ], filters=[time2stamp])
    create_date = IntegerField('文章创建日期', validators=[
        DataRequired(message='change_date不能为空'),
    ], filters=[time2stamp])
    article = StringField('文章内容')
    excerpt = StringField('摘要', validators=[
        DataRequired(message='文章摘要不可为空'),
        Length(max=300, message="摘要最大长度为300")
    ])


class UserValidate(JsonValidate):
    username = StringField('用户名', validators=[
        DataRequired(message='用户名不能为空'),
        Length(min=0, max=128, message="用户名长度在0-128字符间")
    ])
    nickname = StringField('昵称', validators=[
        DataRequired(message='昵称不能为空'),
        Length(min=0, max=128, message="昵称长度在0-128字符间")
    ])
    # TODO 添加验证
    avatar = StringField('头像')
    about = StringField('关于')


class TagValidate(JsonValidate):
    id = IntegerField('标签id', validators=[
        DataRequired(message="id不能为空")])
    name = StringField('标签名', validators=[
        DataRequired(message='标签名不可为空'),
        Length(max=64, message="标签名最大长度为字符")])
    describe = StringField('描述', validators=[Length(min=0, max=128, message="描述长度为0-128字符之间")])


class ResetEmailValidate(JsonValidate):
    email = StringField('邮件', validators=[
        Email(message='请输入有效的邮箱地址，比如：username@domain.com'),
    ])


class ResetPasswordValidate(JsonValidate):
    password = PasswordField('密码', validators=[
        DataRequired(message='密码不可为空'),
        Regexp(r'^[a-zA-Z0-9!@#$%^&*()_+]{6-20}$',
               message='密码长度为6-20个字符,可以为字母,数字,!@#$%^&*()_+')
    ])

# class TagImgValidate(FormValidate):
#     image = FileField('图片', validators=[
#         DataRequired(message='图片不可为空')
#     ])
#     tag_name = StringField('标签名', validators=[
#         DataRequired(message='标签名不能为空')
#     ])
