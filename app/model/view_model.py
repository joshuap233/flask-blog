import json

from flask import current_app, request

from app.model.base import db
from app.model.db import Tag, Post
from app.utils import format_time


# 用于flask jsonify序列化
class BaseView:
    pass


# 格式化从数据库获取的文章
class PostsView(BaseView):
    def __init__(self, posts, page):
        self.posts = self.fill_posts(posts)
        self.page = page,
        self.total = Post.total()

    @staticmethod
    def fill_posts(posts):
        result = []
        for item in posts:
            post = PostView(item).__dict__
            del post['article']
            post['tags'] = ','.join(post['tags'])
            result.append(post)
        return result


class PostView(BaseView):
    def __init__(self, post):
        self.id = post.id
        self.title = post.title or ''
        self.tags = [tag.name for tag in post.tags]
        self.visibility = post.visibility
        self.createDate = format_time(post.create_date)
        self.changeDate = format_time(post.change_date)
        self.article = post.article or ''
        self.comments = post.comments


# 格式化从数据库获取的标签
class TagsView(BaseView):
    def __init__(self, tags, page):
        self.total = Tag.total()
        self.tags = self.fill_tags(tags)
        self.page = page

    @staticmethod
    def fill_tags(tags):
        return [TagView(tag).__dict__ for tag in tags] if tags else []


class TagView(BaseView):
    def __init__(self, tag):
        self.id = tag.id
        self.name = tag.name
        self.describe = tag.describe
        self.count = tag.count


class UserInfoView(BaseView):
    def __init__(self, user):
        self.nickname = user.nickname
        self.username = user.username
        self.email = user.email or ''
        self.about = user.user_about or ''
        self.avatar = user.avatar or ''


# 格式化查询参数
class QueryView:
    def __init__(self):
        query = request.args
        order_by = query.get('orderBy')
        filters = query.get('filters')
        if order_by:
            order_by = json.loads(order_by)
        self.order_by = self._get_order_by(order_by, query.get('orderDirection'))
        if filters:
            filters = json.loads(filters)
        self.filters = filters
        self.page = query.get('page', 1)
        self.pagesize = query.get('pageSize', current_app.config['PAGESIZE'])
        self.search = self._get_search(query.get('search'))

    @staticmethod
    def _get_order_by(order_by, orderDirection):
        if not order_by:
            return db.desc('id')
        # TODO: 默认降序
        field = order_by.get('field')
        # TODO:
        # 列表为可查询字段名,列表为可查询字段名 分别为 标签名与标签的文章数量  文章标题,状态(私密,公开,..),评论数,修改日期,创建日期
        if field and field in ['name', 'count', 'title', 'visibility', 'comments', 'changeDate', 'createDate']:
            return db.desc(field) if orderDirection != 'asc' else db.asc(field)
        return db.desc('id')

    @staticmethod
    def _get_search(search):
        return f"%{search}%" if search else None

# class LoginView:
#     def __init__(self, user):
#         self.username = user.get('username')
#         self.email = user.get('email')
#         self.password = user.get('password')
#         self.query = self._get_query()
#
#     # 判断用邮箱登录(注册)还是用户名登录(注册)
#     def _get_query(self):
#         if self.username:
#             self.type = 'username'
#             return {"username": self.username}
#         if self.email:
#             self.type = 'email'
#             return {"email": self.email}
#         raise ParameterException("请输入用户名或邮箱")
