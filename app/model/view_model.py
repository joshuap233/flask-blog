import json
from urllib.parse import unquote

from flask import current_app, request, url_for

from app.exception import ParameterException
from app.model.baseDB import db
from app.model.db import Tag, Post, Link
from app.utils import format_time
from .baseView import BaseView, TableView


class IdView(BaseView):
    def __init__(self, source):
        self.id = source.id


# 格式化从数据库获取的文章
class PostsView(BaseView, TableView):
    def __init__(self, posts: dict, page: int):
        super().__init__(posts, page, Post)

    @staticmethod
    def _fill(posts):
        result = []
        for item in posts:
            post = PostView(item)
            del post.article
            del post.excerpt
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
        self.excerpt = post.excerpt
        # self.article_html = post.article_html or ''
        # self.excerpt_html = post.article_html or ''
        self.comments = post.comments


# 格式化从数据库获取的标签
class TagsView(BaseView, TableView):
    def __init__(self, tags, page):
        super().__init__(tags, page, Tag)

    @staticmethod
    def _fill(tags):
        return [TagView(tag) for tag in tags] if tags else []


class TagView(BaseView):
    def __init__(self, tag):
        self.id = tag.id
        self.name = tag.name or ''
        self.describe = tag.describe
        self.count = tag.count
        self.image = ImageUrlView(tag.link.url if tag.link else '')


class UserInfoView(BaseView):
    def __init__(self, user):
        self.nickname = user.nickname
        self.username = user.username
        self.email = user.email
        self.about = user.about
        self.about_html = user.about_html
        self.avatar = user.avatar
        self.icp = user.icp
        self.motto = user.motto
        self.set_field_not_None()
        # self.email_is_validate = user.email_is_validate
        self.password = ''


class LoginView(BaseView):
    def __init__(self, user):
        self.id = user.id
        self.token = user.generate_login_token()

    #     if self.check_email_validate(user):
    #         self.msg = '您的邮箱未验证'
    #
    # @staticmethod
    # def check_email_validate(user):
    #     return user.email and not user.email_is_validate


class ImagesView(BaseView, TableView):
    def __init__(self, links, page):
        super().__init__(links, page, Link)

    @staticmethod
    def _fill(links):
        return [ImageView(link) for link in links] if links else []


class NewImagesView(BaseView):
    def __init__(self, links):
        self.values = [NewImageView(link) for link in links]


class NewImageView(BaseView):
    def __init__(self, link):
        self.id = link.id
        self.image = ImageUrlView(link.url)


class ImageView(BaseView):
    def __init__(self, link):
        self.id = link.id
        self.image = ImageUrlView(link.url)
        self.describe = link.describe
        # 图片被使用次数
        self.relationship = self._get_relationship(link)
        self.count = self._get_count()

    def _get_count(self):
        return len(self.relationship)

    @staticmethod
    def _get_relationship(link):
        relationship = [{'id': post.id, 'name': post.title, 'type': '文章'} for post in link.posts]
        relationship.extend([
            {'id': tag.id, 'name': tag.name, 'type': '标签'} for tag in link.tags
        ])
        return relationship


class ImageUrlView(BaseView):
    def __init__(self, filename):
        self.name = filename
        self.url = url_for('admin.send_images_view', filename=filename, _external=True) if filename else ''


class QueryView:
    """
    解析查询参数
    'orderBy':'[{field:'title',desc:True/False}]
    'page':'0',
    'pageSize':'10',
    'search':'str',
    'totalCount':'1',
    'filter_by':{tid:1}
    """
    # TODO:去除硬编码
    # 列表为可排序字段名,分别为 标签名与 标签的文章数量 文章标题 状态(私密,公开,..) 评论数 修改日期 创建日期
    sortable = ['name', 'count', 'title', 'visibility', 'comments', 'change_date', 'create_date']

    # 默认允许 order_by 参数查询
    def __init__(self, order_by=True):
        self.query = request.args
        self.order_by = self._get_order_by() if order_by else None
        self.page = self._get_page()
        self.pagesize = self._get_pagesize()
        self.filters = self._get_filters()

    @property
    def search_parameter(self):
        return dict(
            order_by=self.order_by,
            page=self.page,
            per_page=self.pagesize,
            filters=self.filters
        )

    def _get_page(self):
        # 前端第一页为0,但sqlalchemy分页查询第一页为1
        return int(self.query.get('page', 0)) + 1

    def _get_pagesize(self):
        return int(self.query.get('pageSize', current_app.config['PAGESIZE']))

    def _get_filters(self) -> {}:
        filters = {}
        search = self.query.get('search')
        filters['search'] = f"%{unquote(search)}%" if search else None
        # 支持按标签查找
        try:
            filter_by = json.loads(self.query.get('filter') or '{}')
            tid = int(filter_by.get('tid') or -1)
        except Exception as e:
            raise ParameterException(e.args)
        filters['tid'] = tid if tid and tid > 0 else None
        return filters

    def _get_order_by(self):
        order_bys = self.query.get('orderBy')
        order_by = []
        if not order_bys:
            # 默认按id降序
            order_by.append(db.desc('id'))
        else:
            for ob in order_bys:
                field = order_bys.get('field')
                if field in self.sortable:
                    order_by.append(db.desc(field) if ob.get('desc') else db.asc(field))
        return order_by
