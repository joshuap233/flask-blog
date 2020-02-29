import json

from flask import current_app, request

from app.model.base import db
from app.model.db import Tag, Post
from app.utils import format_time

# 用于flask jsonify序列化
class BaseView:
    # 将None字段设置为''
    def set_field_not_None(self):
        for key, value in self.__dict__.items():
            if value is None:
                setattr(self, key, '')


# 格式化从数据库获取的文章
class PostsView(BaseView):
    def __init__(self, posts, page):
        self.posts = self._fill_posts(posts)
        self.page = page,
        self.total = Post.total()

    @staticmethod
    def _fill_posts(posts):
        result = []
        for item in posts:
            post = PostView(item).__dict__
            del post['article']
            del post['excerpt']
            post['tags'] = ','.join(post['tags'])
            result.append(post)
        return result


class PostView(BaseView):
    def __init__(self, post):
        self.id = post.id
        self.title = post.title or ''
        self.tags = [tag.name for tag in post.tags]
        self.visibility = post.visibility
        self.create_date = format_time(post.create_date)
        self.change_date = format_time(post.change_date)
        self.article = post.article or ''
        self.comments = post.comments
        self.excerpt = post.excerpt


# 格式化从数据库获取的标签
class TagsView(BaseView):
    def __init__(self, tags, page):
        self.total = Tag.total()
        self.tags = self._fill_tags(tags)
        self.page = page

    @staticmethod
    def _fill_tags(tags):
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
        self.email = user.email
        self.about = user.about
        self.avatar = user.avatar
        self.set_field_not_None()


class LoginView(BaseView):
    def __init__(self, user):
        self.id = user.id
        self.token = user.generate_login_token()


# 解析查询参数
class QueryView:
    def __init__(self):
        self.query = request.args
        self.order_by = self._get_order_by()
        self.filters = self._get_filters()
        self.page = self._get_page()
        self.pagesize = self._get_pagesize()
        self.search = self._get_search()

    @property
    def search_parameter(self):
        return dict(
            search=self.search,
            order_by=self.order_by,
            page=self.page,
            per_page=self.pagesize
        )

    def _get_page(self):
        # 前端第一页为0,但sqlalchemy分页查询第一页为1
        return int(self.query.get('page', 0)) + 1

    def _get_pagesize(self):
        return int(self.query.get('pageSize', current_app.config['PAGESIZE']))

    def _get_filters(self):
        filters = self.query.get('filters')
        return json.loads(filters) if filters else filters

    def _get_order_by(self):
        order_by = self.query.get('orderBy')
        orderDirection = self.query.get('orderDirection')
        if not order_by:
            # 默认按id降序
            return db.desc('id')
        order_by = json.loads(order_by)
        field = order_by.get('field')
        # 列表为可查询字段名,分别为 标签名与 标签的文章数量 文章标题 状态(私密,公开,..) 评论数 修改日期 创建日期
        if field and field in ['name', 'count', 'title', 'visibility', 'comments', 'change_date', 'create_date']:
            return db.asc(field) if orderDirection == 'asc' else db.desc(field)
        return db.desc('id')

    def _get_search(self):
        search = self.query.get('search')
        return f"%{search}%" if search else None
