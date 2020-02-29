from sqlalchemy.dialects.mysql import LONGTEXT
from werkzeug.security import check_password_hash, generate_password_hash
from app.exception import AuthFailed
from .base import Base, db
from flask_jwt_extended import create_refresh_token
from flask_jwt_extended import get_jwt_identity
from app.utils import generate_verification_code

tags_to_post = db.Table(
    'tags_to_post',
    db.Column('tags_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True),
    db.Column('post_id', db.Integer, db.ForeignKey('post.id'), primary_key=True)
)

# 文章链接(图片/...)
link_to_post = db.Table(
    'link_to_post',
    db.Column('post_id', db.Integer, db.ForeignKey('post.id'), primary_key=True),
    db.Column('link_id', db.Integer, db.ForeignKey('link.id'), primary_key=True)
)


class Post(Base):
    # 不能用set_attrs方法直接设置的字段列表
    blacklist = ['id', 'comments']
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    article = db.Column(LONGTEXT, nullable=True, comment='文章内容')
    excerpt = db.Column(db.String(300), comment="文章摘要")
    create_date = db.Column(db.BigInteger, index=True)
    change_date = db.Column(db.BigInteger, index=True)
    visibility = db.Column(db.String(16), default="私密", comment='文章可见性:私密/公开')
    comments = db.Column(db.Integer, default=0, comment="评论数量")

    tags = db.relationship('Tag', secondary=tags_to_post, backref=db.backref('posts', lazy='dynamic'))
    links = db.relationship('Link', secondary=link_to_post, backref=db.backref('posts'), lazy='dynamic')

    def __init__(self, *args, **kwargs):
        if 'comments' not in kwargs:
            kwargs['comments'] = self.__table__.c.comments.default.arg
        super().__init__(*args, **kwargs)

    def set_attrs(self, attrs: dict):
        for key, value in attrs.items():
            if key == 'tags':
                self.set_tags(value)
                continue
            if key == 'links':
                self.set_links(value)
                continue
            if hasattr(self, key) and key not in self.blacklist:
                setattr(self, key, value)

    def set_links(self, url):
        self.links.append(Link(url=url))

    def set_tags(self, tags):
        for tag in tags:
            tag = Tag.query.filter_by(name=tag).first() or Tag(name=tag)
            if tag in self.tags:
                continue
            self.tags.append(tag)
            tag.count += 1

    @classmethod
    def delete_by_id(cls, id_):
        one = cls.query.get_or_404(id_)
        with db.auto_commit():
            for tag in one.tags:
                tag.count -= 1
            db.session.delete(one)

    @classmethod
    def search(cls, page, per_page, order_by, **kwargs):
        # TODO: 支持按日期...查找,暂时只支持按文章标题查找
        search = kwargs.get('search')
        if search:
            return cls.query.filter(cls.title.like(search)).order_by(order_by).paginate(
                page=page, per_page=per_page, error_out=False)
        else:
            return cls.query.order_by(order_by).paginate(page=page, per_page=per_page, error_out=False)


class Tag(Base):
    blacklist = ['id', 'count']
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    describe = db.Column(db.String(128), nullable=True)
    # 使用标签的文章数量
    count = db.Column(db.Integer, default=0)
    # 图片链接(用于图床)或图片名(本地)
    picture = db.Column(db.String(255))

    def __init__(self, *args, **kwargs):
        if 'count' not in kwargs:
            kwargs['count'] = self.__table__.c.count.default.arg
        super().__init__(*args, **kwargs)

    @classmethod
    def search(cls, page, per_page, order_by, **kwargs):
        search = kwargs.get('search')
        # TODO: 暂时只支持按标签名查找
        if search:
            return cls.query.filter(
                cls.name.like(search)).order_by(order_by).paginate(
                page=page, per_page=per_page, error_out=False)
        else:
            return cls.query.order_by(order_by).paginate(page=page, per_page=per_page, error_out=False)


class User(Base):
    blacklist = ['id', 'password_hash', 'email']
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(128))
    username = db.Column(db.String(128))
    email = db.Column(db.String(128), nullable=True)
    password_hash = db.Column(db.String(128))
    about = db.Column(LONGTEXT, comment="关于用户")
    avatar = db.Column(LONGTEXT)
    # email_is_validate = db.Column(db.Boolean, default=False)
    # 保留字段
    is_active = db.Column(db.Boolean, default=False)
    # 验证码
    ver_code = db.Column(db.Integer)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        if not check_password_hash(self.password_hash, password):
            raise AuthFailed("密码错误")

    def generate_login_token(self):
        return create_refresh_token(identity=self.id)

    def set_attrs(self, attrs: dict):
        for key, value in attrs.items():
            if key == 'password':
                self.set_password(value)
            if hasattr(self, key) and key not in self.blacklist:
                setattr(self, key, value)

    def is_change_email(self, form):
        return self.email != form.email.data

    @classmethod
    def update_email_by_id(cls, uid, email):
        # 只能用该方法设置邮箱(验证后设置)
        user = cls.query.get_or_404(uid)
        with db.auto_commit():
            user.email = email
            db.session.add(user)

    @classmethod
    def reset_password(cls, form):
        id_ = get_jwt_identity()
        user = cls.query.get_or_404(id_)
        user.check_password(form.old_password.data)
        user.update(password=form.password.data)
        return user

    @classmethod
    def set_ver_code(cls, form):
        user = cls.search_by(email=form.email.data)
        code = generate_verification_code()
        user.update(code=code)
        return code

    @classmethod
    def confirm_ver_code(cls, form):
        code = form.code.data


# 验证码
class Code(Base):
    id = db.Column(db.Integer, primary_key=True)
    ver_code = db.Column(db.Integer)
    create_date = db.Column(db.BigInteger, index=True)
    expire_date = db.Column(db.BigInteger, index=True)


# 用于储存图片链接
class Link(Base):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    describe = db.Column(db.String(255), comment="链接描述")
    # 图片链接(用于图床)或图片名(本地)
    url = db.Column(db.String(255))
