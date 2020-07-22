from abc import ABCMeta, abstractmethod
from urllib.parse import unquote
import json
from flask import current_app, request
from app.model.db import Comment, Blog
from app.utils import format_time
from app.exception import ParameterException


# 用于flask jsonify序列化
class BaseView:
    # 将None字段设置为''
    def set_field_not_None(self):
        for key, value in self.__dict__.items():
            if value is None:
                setattr(self, key, '')


class TableView(metaclass=ABCMeta):
    def __init__(self, values: dict, page: int, model):
        self.values = self._fill(values)
        self.page = page
        self.total = model.total()

    @staticmethod
    @abstractmethod
    def _fill(values) -> []:
        return [value for value in values] if values else []


class BaseQueryView:
    def __init__(self):
        self.queries = request.args
        self.order_by = self._get_order_by()
        self.page = self._get_page()
        self.pagesize = self._get_pagesize()

    @property
    def search_parameter(self):
        return dict(
            order_by=self.order_by,
            page=self.page,
            per_page=self.pagesize,
        )

    @staticmethod
    def _get_order_by() -> list:
        return [{'field': 'change_date'}]

    def _get_pagesize(self) -> int:
        return int(self.queries.get('pageSize', current_app.config['PAGESIZE']))

    def _get_page(self):
        return int(self.queries.get('page', 0)) + 1


class CommentsQueryView(BaseQueryView):
    @staticmethod
    def _get_order_by() -> list:
        return [{'field': 'create_date'}]


class QueryView(BaseQueryView):
    """
    解析查询参数
    'orderBy':'[{field:'title',desc:True/False}]
    'page':'0',
    'pageSize':'10',
    'search':'str',
    'totalCount':'1',
    'filter_by':{tid:1}
    """

    # 默认允许 order_by 参数查询
    def __init__(self):
        super().__init__()
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
        return int(self.queries.get('page', 0)) + 1

    def _get_pagesize(self):
        return int(self.queries.get('pageSize', current_app.config['PAGESIZE']))

    def _get_filters(self) -> {}:
        filters = {}
        search = self.queries.get('search')
        filters['search'] = f"%{unquote(search)}%" if search else None
        # 支持按标签查找
        try:
            filter_by = json.loads(self.queries.get('filter') or '{}')
            tid = int(filter_by.get('tid') or -1)
        except Exception as e:
            raise ParameterException(e.args)
        filters['tid'] = tid if tid and tid > 0 else None
        return filters

    def _get_order_by(self):
        order_by = self.queries.get('orderBy', None)
        if order_by:
            order_by = json.loads(order_by)
        return order_by


class BlogView(BaseView):
    def __init__(self, blog: Blog):
        self.id = blog.id
        self.content = blog.content
        self.change_date = blog.change_date


class BlogsView(BaseView, TableView):
    def __init__(self, comment, page):
        super().__init__(comment, page, Blog)

    @staticmethod
    def _fill(blogs):
        return [BlogView(blog) for blog in blogs] if blogs else []


class BaseComment(BaseView):
    def __init__(self, comment: Comment, show=True, email=True, ip=True):
        self.id = comment.id
        self.content = comment.content
        self.nickname = comment.nickname
        self.browser = comment.browser
        self.system = comment.system
        self.website = comment.website
        self.email = comment.email
        self.create_date = comment.create_date
        if show:
            self.show = comment.show
        if email:
            self.email = comment.email
        if ip:
            self.ip = comment.ip
