from abc import ABCMeta, abstractmethod
from .baseDB import db
import json
from urllib.parse import unquote

from flask import current_app, request

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
    def __init__(self, order_by=True):
        self.query = request.args
        self.order_by = self.query.get('orderBy') if order_by else None
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

    # def _get_order_by(self):
    #     order_bys = self.query.get('orderBy')
    #     order_by = []
    #     if not order_bys:
    #         # 默认按id降序
    #         order_by.append(db.desc('id'))
    #     else:
    #         for ob in order_bys:
    #             field = order_bys.get('field')
    #             if field in self.sortable:
    #                 order_by.append(db.desc(field) if ob.get('desc') else db.asc(field))
    #     return order_by
