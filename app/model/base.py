from contextlib import contextmanager

from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy, BaseQuery

from app.exception import UnknownException, NotFound, ServerException

from app.utils import get_now_timestamp


class SQLAlchemy(_SQLAlchemy):
    @contextmanager
    def auto_commit(self):
        try:
            yield
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise UnknownException(e.args)


class Query(BaseQuery):
    def get_or_404(self, ident, description=None):
        rv = self.get(ident)
        if rv is None:
            raise NotFound()
        return rv

    def first_or_404(self, description=None):
        rv = self.first()
        if rv is None:
            raise NotFound()
        return rv


db = SQLAlchemy(query_class=Query)


# 封装增删改查
class Base(db.Model):
    __abstract__ = True
    # 不能用set_attrs方法直接设置的字段列表
    blacklist = ['id']
    create_date = db.Column(db.BigInteger, index=True)

    def __init__(self, *args, **kwargs):
        self.create_date = get_now_timestamp()
        super(Base, self).__init__(*args, **kwargs)

    def delete(self):
        with db.auto_commit():
            db.session.delete(self)

    @classmethod
    def delete_by_id(cls, id_):
        one = cls.get_or_404(id_)
        with db.auto_commit():
            db.session.delete(one)

    def update(self, attrs: dict = None, **kwargs):
        with db.auto_commit():
            self.set_attrs(attrs)
            self.set_attrs(kwargs)
            db.session.add(self)

    @classmethod
    def update_by_id(cls, id_, attrs: dict = None, **kwargs):
        one = cls.get_or_404(id_)
        with db.auto_commit():
            one.set_attrs(attrs)
            one.set_attrs(kwargs)
            db.session.add(one)

    @classmethod
    def create(cls, attrs: dict = None, **kwargs):
        one = cls()
        with db.auto_commit():
            one.set_attrs(attrs)
            one.set_attrs(kwargs)
            db.session.add(one)
        return one

    @classmethod
    def search_by(cls, attrs: dict = None, **kwargs):
        search = attrs or kwargs
        if len(search) != 1:
            ServerException('参数错误')
        return cls.query.filter_by(**search).first_or_404()

    @classmethod
    def search_by_id(cls, id_):
        return cls.get_or_404(id_)

    # 获取表的记录数
    @classmethod
    def total(cls):
        return cls.query.count()

    def set_attrs(self, attrs: dict):
        if not attrs:
            return
        for key, value in attrs.items():
            self._set_attr(key, value)

    def _set_attr(self, key, value):
        if hasattr(self, key) and key not in self.blacklist:
            setattr(self, key, value)

    @classmethod
    def get_or_404(cls, id_):
        return cls.query.get_or_404(id_)


# 提供搜索功能
class BaseSearch(Base):
    __abstract__ = True

    @classmethod
    def search(cls, page, per_page, order_by, filters, **kwargs):
        search = kwargs.get('search')
        if search:
            return cls.query.filter(filters(search)).order_by(order_by).paginate(
                page=page, per_page=per_page, error_out=False)
        else:
            return cls.query.order_by(order_by).paginate(page=page, per_page=per_page, error_out=False)
