import json
import time

from app.exception import ParameterException
from app.model.base import db
from app.model.db import Tag


# 格式化从数据库获取的文章
class PostsToJsonView:
    def __init__(self, posts):
        self.data = []
        self.posts = posts

    @property
    def json(self):
        if not self.posts:
            return []
        for post in self.posts:
            data: dict = PostToJsonView(post).__dict__
            del data['article']
            data['tags'] = ','.join(data['tags'])
            self.data.append(data)
        return self.data


class PostToJsonView:
    def __init__(self, post):
        self.postId = post.id
        self.title = post.title or ''
        self.tags = [tag.name for tag in post.tags]
        self.visibility = post.visibility
        self.createDate = time.strftime("%Y/%m/%d %H:%M", time.localtime(post.create_date))
        self.changeDate = time.strftime("%Y/%m/%d %H:%M", time.localtime(post.change_date))
        self.article = post.article or ''
        self.comments = post.comments


# 格式化从数据库获取的标签
class TagsToJsonView:
    def __init__(self, tags, page):
        self.tags = tags
        self.page = page

    @property
    def json(self):
        return {
            'total': Tag.total(),
            'page': self.page,
            'tags': [TagToJsonView(tag).__dict__ for tag in self.tags] if self.tags else []
        }


class TagToJsonView:
    def __init__(self, tag):
        self.tagId = tag.id
        self.name = tag.name
        self.describe = tag.describe
        self.count = tag.count


# 格式化从前端获取的查询参数
class QueryView:
    def __init__(self, query):
        orderBy = query.get('orderBy')
        filters = query.get('filters')
        if orderBy:
            orderBy = json.loads(orderBy)
        self.orderBy = self._getOrderByField(orderBy, query.get('orderDirection'))
        if filters:
            filters = json.loads(filters)
        self.filters = filters
        # TODO: 设置默认第一页,每页10条记录(写入配置
        self.page = int(query.get('page', 1))
        self.pageSize = int(query.get('pageSize', 10))
        self.search = self._getSearch(query.get('search'))

    @staticmethod
    def _getOrderByField(orderBy, orderDirection):
        if not orderBy:
            return db.desc('id')
        # TODO: 默认降序
        field = orderBy.get('field')
        # 列表为可查询字段名,列表为可查询字段名 分别为 标签名与标签的文章数量  文章标题,状态(私密,公开,..),评论数,修改日期,创建日期
        if field and field in ['name', 'count', 'title', 'visibility', 'comments', 'changeDate', 'createDate']:
            return db.desc(field) if orderDirection != 'asc' else db.asc(field)
        return db.desc('id')

    @staticmethod
    def _getSearch(search):
        return f"%{search}%" if search else None


# 格式化从前端接收的文章
class JsonToPostView:
    def __init__(self, post):
        if not post:
            return
        self.id = post.get('postId')
        self.title = post.get('title')
        self.tags = post.get('tags')
        self.visibility = post.get('visibility')
        if post.get('createDate'):
            self.create_date = time.mktime(time.strptime(post.get('createDate'), '%Y/%m/%d %H:%M'))
        if post.get('changeDate'):
            self.change_date = time.mktime(time.strptime(post.get('changeDate'), '%Y/%m/%d %H:%M'))
        self.article = post.get('article')


# 格式化从前端接收的标签
class JsonToTagView:
    def __init__(self, tag):
        if not tag:
            return
        self.id = tag.get('tagId', -1)
        self.name = tag.get('name')
        self.describe = tag.get('describe')


class UserInfoView:
    def __init__(self, user):
        self.nickname = user.nickname
        self.username = user.username
        self.email = user.email or ''
        self.about = user.user_about or ''
        self.avatar = user.avatar or ''


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
