import json
import time

from app.model.db import db, Tag


class Base:
    def fill(self):
        return self.__dict__


# 格式化从数据库获取的文章
class PostsToJsonView(Base):
    def __init__(self, posts):
        self.data = []
        self.posts = posts

    def fill(self):
        if not self.posts:
            return []
        for post in self.posts:
            data: dict = PostToJsonView(post).fill()
            del data['article']
            data['tags'] = ','.join(data['tags'])
            self.data.append(data)
        return self.data


class PostToJsonView(Base):
    def __init__(self, post):
        self.postId = int(post.id)
        self.title = post.title or ''
        self.tags = [tag.name for tag in post.tags]
        self.visibility = post.visibility
        self.createDate = time.strftime("%Y/%m/%d %H:%M", time.localtime(post.create_date))
        self.changeDate = time.strftime("%Y/%m/%d %H:%M", time.localtime(post.change_date))
        self.article = post.article or ''
        self.comments = post.comments


# 格式化从数据库获取的标签
class TagsToJsonView(Base):
    def __init__(self, tags, page):
        self.tags = tags
        self.page = page

    def fill(self):
        return {
            'total': Tag.total(),
            'page': self.page,
            'tags': [TagToJsonView(tag).fill() for tag in self.tags] if self.tags else []
        }


class TagToJsonView(Base):
    def __init__(self, tag):
        self.tagId = int(tag.id or -1)
        self.name = tag.name
        self.describe = tag.describe
        self.count = tag.count


# 格式化从前端获取的查询参数
class QueryView(Base):
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
        self.page = int(query.get('page') or 1)
        self.pageSize = int(query.get('pageSize') or 10)
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
class JsonToPostView(Base):
    def __init__(self, post):
        if not post:
            return
        self.id = int(post.get('postId') or -1)
        self.title = post.get('title')
        self.tags = post.get('tags')
        self.visibility = post.get('visibility')
        if post.get('createDate'):
            self.create_date = time.mktime(time.strptime(post.get('createDate'), '%Y/%m/%d %H:%M'))
        if post.get('changeDate'):
            self.change_date = time.mktime(time.strptime(post.get('changeDate'), '%Y/%m/%d %H:%M'))
        self.article = post.get('article')


# 格式化从前端接收的标签
class JsonToTagView(Base):
    def __init__(self, tag):
        if not tag:
            return
        self.id = int(tag.get('tagId') or -1)
        self.name = tag.get('name')
        self.describe = tag.get('describe')


class JsonToUserView(Base):
    def __init__(self, user: dict):
        # 注册时,输入用户名密码注册用户,返回用户id,添加邮箱或手机时,前段添加userId字段
        self.id = int(user.get('userId') or -1)
        # 登录方式 没有则默认用户名登录
        self.nickname = user.get('nickname')
        self.username = user.get('username')
        self.email = user.get('email')
        self.password = user.get('password')
        # str(None) == 'None'
        phone = user.get('phone')
        if phone:
            self.phone = str(phone)
        self.user_about = user.get('user_about')
        self.query = self._get_query()

    # 判断用邮箱登录(注册)还是用户名登录(注册)
    def _get_query(self):
        if self.username:
            self.type = 'username'
            return {"username": self.username}
        if self.email:
            self.type = 'email'
            return {"email": self.email}
        return None
