from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from sqlalchemy.dialects.mysql import LONGTEXT
from werkzeug.security import check_password_hash, generate_password_hash

from app import db

tags_to_post = db.Table(
    'tags_to_post',
    db.Column('tags_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True),
    db.Column('post_id', db.Integer, db.ForeignKey('post.id'), primary_key=True)
)


class Base(db.Model):
    __abstract__ = True

    def auto_add(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()

    def auto_delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()

    # 获取表的记录数
    @classmethod
    def total(cls):
        return cls.query.count()


class Post(Base):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    article = db.Column(LONGTEXT, nullable=True)
    create_date = db.Column(db.BigInteger, index=True)
    change_date = db.Column(db.BigInteger, index=True)
    visibility = db.Column(db.String(16), default="私密")
    # 评论数量
    comments = db.Column(db.Integer, default=0)
    tags = db.relationship('Tag', secondary=tags_to_post, backref=db.backref('posts', lazy='dynamic'))

    def __init__(self, *args, **kwargs):
        if 'comments' not in kwargs:
            kwargs['comments'] = self.__table__.c.comments.default.arg
        super().__init__(*args, **kwargs)

    def set_attrs(self, attrs: dict):
        blacklist = ['id', 'tags', 'comments']
        for key, value in attrs.items():
            if hasattr(self, key) and key not in blacklist:
                setattr(self, key, value)


class Tag(Base):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    describe = db.Column(db.String(128), nullable=True)
    # 使用标签的文章数量
    count = db.Column(db.Integer, default=0)

    def __init__(self, *args, **kwargs):
        if 'count' not in kwargs:
            kwargs['count'] = self.__table__.c.count.default.arg
        super().__init__(*args, **kwargs)

    def set_attrs(self, attrs: dict):
        blacklist = ['id', 'count']
        for key, value in attrs.items():
            if hasattr(self, key) and key not in blacklist:
                setattr(self, key, value)


class User(Base):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    nickname = db.Column(db.String(128))
    username = db.Column(db.String(128))
    email = db.Column(db.String(128))
    phone = db.Column(db.String(32))
    password_hash = db.Column(db.String(128))
    user_about = db.Column(LONGTEXT)
    avatar = db.Column(LONGTEXT)
    # 是否登录(无法强制使jwt失效,只能通过该字段控制)
    is_active = db.Column(db.Boolean, default=False)
    # 注册是否验证
    email_is_validate = db.Column(db.Boolean, default=False)
    phone_is_validate = db.Column(db.Boolean, default=False)

    def generate_password_hash(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'id': self.id}).decode('utf-8')

    def confirm_token(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        if data.get('id') != self.id:
            return False
        return True

    @classmethod
    def confirm_email_token(cls, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        data = s.loads(token.encode('utf-8'))
        user = cls.query.get(data.get('id'))
        if user and not user.email_is_validate:
            user.email_is_validate = True
            user.auto_add()
            return True
        return False

    def set_attrs(self, attrs: dict):
        blacklist = ['id', 'is_validate', 'is_validate', 'password_hash', 'email', 'phone']
        for key, value in attrs.items():
            if hasattr(self, key) and key not in blacklist:
                setattr(self, key, value)
            if key == 'password':
                self.generate_password_hash(value)
