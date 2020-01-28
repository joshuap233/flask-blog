import time

from app.model.db import db


# 格式化从数据库获取的文章
class PostsToJsonView:
    def __init__(self, posts):
        self.data = []
        self.posts = posts

    def fill(self):
        if not self.posts:
            return []
        for post in self.posts:
            data = PostToJsonView(post).__dict__
            data['tags'] = ','.join(data['tags'])
            self.data.append(data)
        return self.data


class PostToJsonView:
    def __init__(self, post):
        self.postId = int(post.id)
        self.title = post.title
        self.tags = [tag['name'] for tag in post.tags]
        self.visibility = post.visibility
        self.createDate = time.strftime("%Y/%m/%d %H:%M", time.localtime(post.createDate))
        self.changeDate = time.strftime("%Y/%m/%d %H:%M", time.localtime(post.changeDate))
        self.article = post['article']


# 格式化从数据库获取的标签
class TagsToJsonView:
    def __init__(self, tags):
        self.tags = tags

    def fill(self):
        return [TagToJsonView(tag).__dict__ for tag in self.tags] if not self.tags else []


class TagToJsonView:
    def __init__(self, tag):
        self.tagId = int(tag.id)
        self.name = tag.name
        self.describe = tag.describe
        self.count = tag.count


# 格式化从前端获取的查询参数
class QueryView:
    def __init__(self, query):
        # TODO: 设置默认第一页,每页10条记录(写入配置
        self.page = int(query.get('page')) or 1
        self.pageSize = int(query.get('pageSize')) or 10
        self.search = self._getSearch(query.get('search'))
        self.orderBy = self._getOrderByField(query.get('orderBy'), query.get('orderDirection'))

    @staticmethod
    def _getOrderByField(orderBy, orderDirection):
        # TODO: 默认降序
        field = orderBy.get('filed')
        # 列表为可查询字段名,列表为可查询字段名 分别为 标签名与标签的文章数量  文章标题,状态(私密,公开,..),评论数,修改日期,创建日期
        if field and field in ['name', 'count', 'title', 'visibility', 'comments', 'changeDate', 'createDate']:
            return db.desc(field) if orderDirection != 'asc' else db.asc(field)
        return db.desc()

    @staticmethod
    def _getSearch(search):
        return f"%{search}%" if search else None


# 格式化从前端接收的文章
class JsonToPostView:
    def __init__(self, post):
        if not post:
            return
        self.id = int(post.get('id'))
        self.title = post.get('title')
        self.tags = post.get('tags')
        self.visibility = post.get('visibility')
        self.createDate = time.mktime(time.strptime(post.get('createDate'), '%Y/%m/%d %H:%M'))
        self.changeDate = time.mktime(time.strptime(post.get('changeDate'), '%Y/%m/%d %H:%M'))
        self.article = post['article']


# 格式化从前端接收的标签
class JsonToTagView:
    def __init__(self, tag):
        if not tag:
            return
        self.id = int(tag.get('tagId'))
        self.name = tag.get('name')
        self.describe = tag.get('describe')
        self.count = int(tag.get('count'))
