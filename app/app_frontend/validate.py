from app.model.validateBase import JsonValidate
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, Email, Length, Optional
from app.exception import ParameterException


# TODO 过滤字符串
class CommentValidate(JsonValidate):
    content = StringField('评论', validators=[
        DataRequired(message="评论不能为空"),
        # Length(min=0, max=255, message="评论长度超过最大值"),
    ])
    ip = StringField('ip', validators=[
        Length(min=0, max=16, message="ip长度超过最大值"),
    ])
    nickname = StringField('email', validators=[
        DataRequired(message="昵称不能为空"),
        Length(min=0, max=20, message="昵称长度超过最大值"),
    ])
    browser = StringField('email', validators=[
        Length(min=0, max=48, message="浏览器类型长度超出最大值"),
    ])
    system = StringField('email', validators=[
        Length(min=0, max=12, message="操作系统长度超限"),
    ])
    website = StringField('email', validators=[
        Length(min=0, max=256, message="网站长度超限"),
    ])
    comment_id = IntegerField('文章评论的回复id')
    parent_id = IntegerField('回复的父评论id')
    email = StringField('email', validators=[
        Email(message='请输入有效的邮箱地址，比如：example@gmail.com'),
        Length(min=0, max=256, message="email长度超过最大值"),
        Optional()
    ])

    def validate(self, extra_validators=None):
        # if not (self.comment_id.data or self.parent_id.data):
        #     raise ParameterException(msg='参数错误')
        super(CommentValidate, self).validate()
