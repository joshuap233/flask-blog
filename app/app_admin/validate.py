from wtforms import PasswordField, StringField, IntegerField, FieldList, BooleanField
from wtforms.validators import DataRequired, EqualTo, Regexp, Email, Length, AnyOf, Optional

from app.config.constant import VERIFICATION_CODE_LENGTH
from app.exception import ParameterException
from app.model.baseDB import Visibility
from app.model.validateBase import JsonValidate
from app.utils import time2stamp


class LoginValidate(JsonValidate):
    password = PasswordField('密码', validators=[
        DataRequired(message="密码不可为空"),
        Regexp(r'^^[a-zA-Z0-9!.@#$%^&*()_+]{6,20}$',
               message='用户名或密码错误'),
    ])
    username = StringField('用户名', validators=[
        Length(min=0, max=128, message="用户名或密码错误"),
    ])
    email = StringField('邮件', validators=[
        Email(message='请输入有效的邮箱地址，比如：username@domain.com'),
        Length(min=0, max=256, message="email长度超过最大值"),
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
        Regexp(r'^[a-zA-Z0-9.!@#$%^&*()_+]{6,20}$',
               message='密码长度为6-20个字符,可以为字母,数字,.!@#$%^&*()_+'),
    ])
    confirm_password = PasswordField('确认密码', validators=[
        DataRequired(message='请确认密码'),
        EqualTo('password', message='两次输入密码不一致')

    ])
    email = StringField('邮件', validators=[
        Email(message='请输入有效的邮箱地址，比如：username@domain.com'),
        Optional()
    ])


class PostValidate(JsonValidate):
    title = StringField('文章标题', validators=[
        Length(0, 128, message="文章标题在0~128字符之间")
    ])
    tags = FieldList(StringField('标签'), min_entries=0)
    visibility = StringField('文章可见性', validators=[
        DataRequired(message='visibility不能为空'),
        AnyOf(
            [Visibility.privacy.value, Visibility.public.value],
            message="visibility只能为私密或公开"
        )
    ])
    change_date = IntegerField('文章修改日期', validators=[
        DataRequired(message='change_date不能为空'),
    ], filters=[time2stamp])
    create_date = IntegerField('文章创建日期', validators=[
        DataRequired(message='create_date不能为空'),
    ], filters=[time2stamp])

    article = StringField('文章内容')
    article_html = StringField('文章内容')

    isRichText = BooleanField('摘要是否为富文本')
    excerpt = StringField('摘要')
    # base64
    illustration = StringField('摘录插图')
    # BooleanField 不能加dataRequired,否则值为False会直接验证错误,显示没有这个值,真的坑.....
    illustration_changed = BooleanField('验证插图是否改变,防止重复添加')
    excerpt_rich_text_html = StringField('摘录/富文本的html')
    excerpt_rich_text = StringField('摘录/富文本')


class UserValidate(JsonValidate):
    username = StringField('用户名', validators=[
        DataRequired(message='用户名不能为空'),
        Length(min=0, max=128, message="用户名长度在0-128字符间")
    ])
    nickname = StringField('昵称', validators=[
        DataRequired(message='昵称不能为空'),
        Length(min=0, max=128, message="昵称长度在0-128字符间")
    ])

    icp = StringField('备案号', validators=[
        Length(min=0, max=128, message="昵称长度在0-128字符间")
    ])
    motto = StringField('座右铭', validators=[
        Length(min=0, max=128, message="昵称长度在0-128字符间")
    ])
    avatar = StringField('头像')
    # TODO 添加验证
    about = StringField('关于')
    about_html = StringField('关于')


class TagValidate(JsonValidate):
    name = StringField('标签名', validators=[
        DataRequired(message='标签名不可为空'),
        Length(max=64, message="标签名最大长度为字符")])
    describe = StringField('描述', validators=[
        Length(min=0, max=128, message="描述长度为0-128字符之间")
    ])


class DeleteValidate(JsonValidate):
    id_list = FieldList(IntegerField('标签id'), min_entries=1)


class EmailValidate(JsonValidate):
    email = StringField('邮件', validators=[
        Email(message='请输入有效的邮箱地址，比如：username@domain.com'),
    ])


class EmailCodeValidate(JsonValidate):
    # TODO: 验证码长度🌿配置
    code = StringField('验证码', filters=[str], validators=[
        Length(VERIFICATION_CODE_LENGTH, VERIFICATION_CODE_LENGTH, message='验证码错误')
    ])
    email = StringField('邮件', validators=[
        Email(message='请输入有效的邮箱地址，比如：username@domain.com'),
    ])


class ResetPasswordValidate(JsonValidate):
    old_password = PasswordField('密码', validators=[
        DataRequired(message='密码不可为空'),
        Regexp(r'^[a-zA-Z0-9.!@#$%^&*()_+]{6,20}$',
               message='密码长度为6-20个字符,可以为字母,数字,.!@#$%^&*()_+')
    ])
    password = PasswordField('密码', validators=[
        DataRequired(message='密码不可为空'),
        Regexp(r'^[a-zA-Z0-9.!@#$%^&*()_+]{6,20}$',
               message='密码长度为6-20个字符,可以为字母,数字,.!@#$%^&*()_+')
    ])
    confirm_password = PasswordField('确认密码', validators=[
        DataRequired(message='请确认密码'),
        EqualTo('password', message='两次输入密码不一致')
    ])


class RecoveryPasswordValidate(JsonValidate):
    code = StringField('验证码', filters=[str], validators=[
        Length(VERIFICATION_CODE_LENGTH, VERIFICATION_CODE_LENGTH, message='验证码错误')
    ])
    email = StringField('邮件', validators=[
        Email(message='请输入有效的邮箱地址，比如：username@domain.com'),
    ])
    password = PasswordField('密码', validators=[
        DataRequired(message='密码不可为空'),
        Regexp(r'^[a-zA-Z0-9.!@#$%^&*()_+]{6,20}$',
               message='密码长度为6-20个字符,可以为字母,数字,.!@#$%^&*()_+')
    ])
    confirm_password = PasswordField('确认密码', validators=[
        DataRequired(message='请确认密码'),
        EqualTo('password', message='两次输入密码不一致')
    ])


class ChangeImageValidate(JsonValidate):
    describe = StringField('摘要', validators=[
        Length(max=255, message="描述最大长度为300")
    ])


class DeleteCommentValidate(JsonValidate):
    id_list = FieldList(IntegerField('需要删除的评论id'), min_entries=1)


class CommentValidate(JsonValidate):
    show = BooleanField('显示/隐藏')


class ModifyBlog(JsonValidate):
    id = IntegerField('需要修改的日志id', validators=[
        DataRequired(message='不能为空'),
    ])

    content = StringField(
        Length(0, 255, message='日志最大长度为255')
    )
    isNew = BooleanField('是否是新日志')
    change_date = IntegerField('日志修改日期', validators=[
        DataRequired(message='日志修改日期不能为空'),
    ], filters=[time2stamp])


class DeleteBlog(JsonValidate):
    id_list = FieldList(IntegerField('需要删除的日志id'), min_entries=1)
