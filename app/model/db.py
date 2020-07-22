from functools import reduce

from flask_jwt_extended import create_refresh_token, get_jwt_identity
from sqlalchemy.dialects.mysql import LONGTEXT
from werkzeug.security import check_password_hash, generate_password_hash

from app.exception import AuthFailed, ValidateCodeException, RepeatException, UserHasRegister
from app.myType import WTForm
from app.utils import generate_verification_code, get_code_exp_stamp, get_now_timestamp
from .baseDB import Base, db, Searchable, Visibility, Query

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


class Post(Searchable):
    # 不能用set_attrs方法直接设置的字段列表
    blacklist = ['id', 'illustration_id']

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), default='')
    # 用于编辑
    article = db.Column(LONGTEXT, comment='文章内容(json)', default='')
    # 用于渲染
    article_html = db.Column(LONGTEXT, comment='文章内容(html)', default='')
    change_date = db.Column(db.BigInteger, index=True)
    comments = db.Column(db.Integer, default=0, comment="评论数量")

    excerpt = db.Column(db.String(300), comment="文章摘要(普通文本)", default='')
    # 用于渲染
    excerpt_rich_text_html = db.Column(db.TEXT, comment='文章摘要(富文本)(html)', default='')
    # 摘录普通文本用于编辑
    excerpt_rich_text = db.Column(db.TEXT, comment="文章摘要(富文本)(json)", default='')
    visibility = db.Column(db.String(16), default=Visibility.privacy.value, comment='文章可见性:私密/公开')
    # 摘录插图.一对一
    illustration_id = db.Column(db.Integer, db.ForeignKey('link.id'), comment='插图链接id')
    isRichText = db.Column(db.Boolean, default=False, comment='摘录是否为富文本')
    tags = db.relationship('Tag', secondary=tags_to_post, backref=db.backref('posts', lazy='dynamic'))
    # 文章图片
    links = db.relationship('Link', secondary=link_to_post, backref=db.backref('posts', lazy=True))
    # 评论,前面名字取错,懒得改了
    comments_ = db.relationship(
        'Comment',
        backref=db.backref('posts', lazy=True),
        cascade="all, delete-orphan",
        passive_deletes=True,
        lazy='dynamic'
    )
    # 可排序字段
    sortable = ['change_date', 'create_date', 'title', 'visibility', 'comments']

    def __init__(self, *args, **kwargs):
        if 'comments' not in kwargs:
            kwargs['comments'] = self.__table__.c.comments.default.arg
        super().__init__(*args, **kwargs)

    def _set_attrs(self, attrs: dict):
        for key, value in attrs.items():
            if key == 'tags':
                self._set_tags(value)
            elif key == 'links':
                self._set_links(value)
            elif key == 'illustration':
                self._set_illustration(value)
            else:
                self._set_attr(key, value)

    def _set_illustration(self, url: str):
        self.illustration = Link(url=url)

    def _set_links(self, url: str):
        self.links.append(Link(url=url))

    def _set_tags(self, tags: dict):
        # 移除被删除的标签
        for t in self.tags:
            if t.name not in tags:
                t.count -= 1
                self.tags.remove(t)
        for tag in tags:
            # 添加新标签
            tag = Tag.search_by(name=tag, error=False) or Tag(name=tag)
            if tag in self.tags:
                continue
            self.tags.append(tag)
            tag.count += 1

    @classmethod
    def total(cls, visibility: Visibility = Visibility.public.value):
        if visibility == Visibility.public.value:
            return cls.visibility_posts().total()
        return super().total()

    @classmethod
    def visibility_posts(cls):
        return cls.query.filter_by(visibility=Visibility.public.value)

    @classmethod
    def delete_by_id(cls, identify: int):
        one = cls.search_by(id=identify)
        with db.auto_commit():
            for tag in one.tags:
                tag.count -= 1
            db.session.delete(one)

    @classmethod
    def paging_search(cls, page: int, per_page: int, query: Query = None, filters: [dict, None] = None, order_by=None):
        search = filters.get('search') if filters else None
        query = query or cls.query
        if search:
            queries = [cls.query.filter(cls.title.like(search)), *[
                tag.posts for tag in Tag.query.filter(Tag.name.like(search)).all()
            ]]
            query = reduce(lambda pre, next_: pre.union(next_), queries, query)
        return super().paging_search(query=query, page=page, per_page=per_page, order_by=order_by)

    @classmethod
    def paging_by_tid(cls, tid: int, visibility: bool, **kwargs):
        query = Tag.search_by(id=tid).posts
        if visibility:
            query = query.filter_by(visibility=visibility)
        return super().paging_search(query=query, **kwargs)


class Tag(Searchable):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    describe = db.Column(db.String(128), default='')
    # 使用标签的文章数量
    count = db.Column(db.Integer, default=0)
    # 图片链接(用于图床)或图片名(本地)
    link_id = db.Column(db.Integer, db.ForeignKey('link.id'))

    sortable = ['name', 'create_date']

    def __init__(self, *args, **kwargs):
        if 'count' not in kwargs:
            kwargs['count'] = self.__table__.c.count.default.arg
        super().__init__(*args, **kwargs)

    @classmethod
    def paging_search(cls, page: int, per_page: int, query: Query = None, filters: [dict, None] = None, order_by=None):
        search = filters.get('search') if filters else None
        query = query or cls.query
        if search:
            filters_ = [cls.name.like(search), cls.describe.like(search)]
            queries = [cls.query.filter(filter_) for filter_ in filters_]
            query = reduce(lambda pre, next_: pre.union(next_), queries, query) if queries else query
        return super().paging_search(query=query, page=page, per_page=per_page, order_by=order_by)

    # 更新标签名时查重
    @classmethod
    def check_repeat(cls, **kwargs):
        one = cls.search_by(**kwargs, error=False)
        if one:
            raise RepeatException(msg='标签名已存在')

    def _set_link(self, url):
        self.link = Link(url=url)

    def _set_attrs(self, attrs: dict):
        for key, value in attrs.items():
            if key == 'link':
                self._set_link(value)
                continue
            self._set_attr(key, value)

    @classmethod
    def total(cls, visibility: bool = False):
        if not visibility:
            return super().total()
        return cls.visibility_tags().total()

    @classmethod
    def visibility_tags(cls):
        # query = Tag.query.filter(Tag.posts.has(visibility=Visibility.public.value'))
        return Tag.query.join(Tag.posts, aliased=True).filter_by(visibility=Visibility.public.value)


class User(Base):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(128))
    username = db.Column(db.String(128))
    email = db.Column(db.String(128), nullable=True)
    password_hash = db.Column(db.String(128))
    about = db.Column(LONGTEXT, comment="关于用户(json raw)")
    about_html = db.Column(LONGTEXT, comment="关于用户(html)")
    avatar = db.Column(LONGTEXT)
    motto = db.Column(db.String(128))
    icp = db.Column(db.String(128))
    # 保留字段
    email_is_validate = db.Column(db.Boolean, default=False)
    # 验证码
    code = db.relationship('Code', backref=db.backref('user', lazy=True), uselist=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str):
        if not check_password_hash(self.password_hash, password):
            raise AuthFailed("密码错误")

    def generate_login_token(self):
        return create_refresh_token(identity=self.id)

    def _set_attrs(self, attrs: dict):
        for key, value in attrs.items():
            if key == 'password':
                self.set_password(value)
                continue
            self._set_attr(key, value)

    @classmethod
    def reset_password(cls, form: WTForm):
        """登录状态下调用"""
        uid = get_jwt_identity()
        user = cls.search_by(id=uid)
        user.update(password=form.password.data)
        return user

    @classmethod
    def validate_code_by(cls, code: str, **kwargs):
        user = cls.search_by(**kwargs)
        user.code.validate_code(code)
        return user

    def set_code(self):
        code = Code()
        self.update(code=code)
        return code.code

    @classmethod
    def set_code_by_id(cls):
        identify = get_jwt_identity()
        user = cls.search_by(id=identify)
        return user.set_code()

    # 登录状态调用
    @classmethod
    def get_user(cls):
        uid = get_jwt_identity()
        return cls.search_by(id=uid)

    @classmethod
    def check_register(cls):
        user = cls.query.all()
        if user:
            raise UserHasRegister('用户已注册')


# 验证码
class Code(Base):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(16))
    expire_date = db.Column(db.BigInteger, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, *args, **kwargs):
        self.code = generate_verification_code()
        self.expire_date = get_code_exp_stamp()
        super(Code, self).__init__(*args, **kwargs)

    @property
    def _is_expire(self):
        now = get_now_timestamp()
        return now > self.expire_date

    def _set_code_expire(self):
        expire_date = get_now_timestamp() - 1
        self.update(expire_date=expire_date)

    def validate_code(self, code: str):
        if self.code != code:
            raise ValidateCodeException("验证码错误")
        if self._is_expire:
            raise ValidateCodeException("验证码已过期")
        self._set_code_expire()

    def _set_attrs(self, attrs: dict):
        super()._set_attrs(attrs)


# 用于储存图片链接
class Link(Searchable):
    id = db.Column(db.Integer, primary_key=True)
    describe = db.Column(db.String(255), comment="链接描述")
    # 图片链接(用于图床)或图片名(本地)
    url = db.Column(db.String(255))
    tags = db.relationship('Tag', backref=db.backref('link', lazy=True))
    post_illustration = db.relationship('Post', backref=db.backref('illustration', lazy=True), uselist=False)
    sortable = ['create_date']

    @classmethod
    def paging_search(cls, page: int, per_page: int, query: Query = None, filters: [dict, None] = None, order_by=None):
        search = filters.get('search')
        query = query or cls.query
        if search:
            filters_ = [cls.describe.like(search)]
            queries = [cls.query.filter(filter_) for filter_ in filters_]
            query = reduce(lambda pre, next_: pre.union(next_), queries, query) if queries else query
        return super().paging_search(query=query, page=page, per_page=per_page, order_by=order_by)

    def _set_attrs(self, attrs: dict):
        super()._set_attrs(attrs)


# 记录日常吐槽
class Blog(Searchable):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(255), comment="内容")
    change_date = db.Column(db.BigInteger, index=True)

    def _set_attrs(self, attrs: dict):
        super()._set_attrs(attrs)

    @classmethod
    def paging_search(cls, page: int, per_page: int, query: Query = None, filters: [dict, None] = None, order_by=None):
        return super().paging_search(query=query, page=page, per_page=per_page, order_by=order_by)


class BaseComment(Searchable):
    __abstract__ = True

    content = db.Column(db.TEXT, comment="评论内容")
    ip = db.Column(db.String(16), comment="ip地址")
    email = db.Column(db.String(256), comment="邮件地址")
    nickname = db.Column(db.String(20), comment="昵称")
    website = db.Column(db.String(256), comment="网站")
    show = db.Column(db.Boolean, default=False, comment="评论是否显示/用于审核")
    avatar = db.Column(db.String(256), comment='头像')
    # ua?
    browser = db.Column(db.String(48), comment="浏览器类型/版本")
    system = db.Column(db.String(12), comment="操作系统")

    def _set_attrs(self, attrs: dict):
        super()._set_attrs(attrs)

    @classmethod
    def paging_search(cls, page: int, per_page: int, query: Query = None, order_by=None):
        return super().paging_search(query=query, page=page, per_page=per_page, order_by=order_by)


# 文章下的评论
class Comment(BaseComment):
    blacklist = ['id', 'comment_reply']

    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id', ondelete='CASCADE'))
    comment_reply = db.relationship('CommentReply', cascade="all, delete-orphan", passive_deletes=True, lazy='dynamic')

    def _set_attrs(self, attrs: dict):
        super()._set_attrs(attrs)

    @classmethod
    def paging_search(cls, page: int, per_page: int, order_by: dict = None, query: Query = None):
        query = cls.query.union(CommentReply.query)
        return super().paging_search(page=page, per_page=per_page, order_by=order_by, query=query)

    @staticmethod
    def update_comment(**kwargs):
        modal = CommentReply if (kwargs.get('parent_id', None) or kwargs.get('comment_id')) else Comment
        return modal.create(**kwargs)


# 评论的回复/回复的回复
class CommentReply(BaseComment):
    blacklist = ['id']

    id = db.Column(db.Integer, primary_key=True)
    comment_id = db.Column(
        db.Integer,
        db.ForeignKey('comment.id', ondelete='CASCADE'),
        comment="文章评论的回复的id",
        nullable=False
    )
    parent_id = db.Column(db.Integer, comment="回复的回复id", nullable=True)

    def _set_attrs(self, attrs: dict):
        super()._set_attrs(attrs)

    @classmethod
    def paging_search(cls, page: int, per_page: int, query: Query = None, filters: [dict, None] = None, order_by=None):
        return super().paging_search(query=query, page=page, per_page=per_page, order_by=order_by)
