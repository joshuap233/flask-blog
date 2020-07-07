from abc import ABCMeta, abstractmethod
from urllib.parse import unquote
import json
from flask import current_app, request
from app.model.db import Comment, CommentReply, Blog

from app.exception import ParameterException


# 用于flask jsonify序列化
class BaseView:
    # 将None字段设置为''
    def set_field_not_None(self):
        for key, value in self.__dict__.items():
            if value is None:
                setattr(self, key, '')


class TableView(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, values: dict, page: int, model):
        self.values = self._fill(values)
        self.page = page
        self.total = model.total()

    @staticmethod
    @abstractmethod
    def _fill(values) -> []:
        return [value for value in values] if values else []


class BaseQueryView(metaclass=ABCMeta):
    def __init__(self):
        self.query = request.args
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
    @abstractmethod
    def _get_order_by() -> list:
        return []

    @staticmethod
    @abstractmethod
    def _get_pagesize() -> int:
        return 1

    def _get_page(self):
        return int(self.query.get('page', 0)) + 1


class CommentQueryView(BaseQueryView):
    @staticmethod
    def _get_order_by():
        return [Comment.create_date.desc()]

    @staticmethod
    def _get_pagesize() -> int:
        return current_app.config['COMMENT_PAGE_SIZE']


class ReplyQueryView(BaseQueryView):
    @staticmethod
    def _get_order_by():
        return [CommentReply.create_date.desc()]

    @staticmethod
    def _get_pagesize() -> int:
        return current_app.config['SUB_COMMENT_PAGE_SIZE']


class BlogQueryView(BaseQueryView):
    @staticmethod
    def _get_order_by():
        return [Blog.create_date.desc()]

    @staticmethod
    def _get_pagesize() -> int:
        return current_app.config['BLOG_PAGE_SIZE']


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

    # 默认允许 order_by 参数查询
    def __init__(self):
        self.query = request.args
        self.order_by = self._get_order_by()
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
        order_by = self.query.get('orderBy', None)
        if order_by:
            order_by = json.loads(order_by)
        return order_by
