from contextlib import contextmanager

from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy, BaseQuery

from app.exception import UnknownException, NotFound


class SQLAlchemy(_SQLAlchemy):
    @contextmanager
    def auto_commit(self):
        try:
            yield
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise UnknownException


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
    blacklist = []

    @classmethod
    def create(cls, attrs: dict = None, **kwargs):
        one = cls()
        with one.auto_commit():
            one.set_attrs(attrs)
            one.set_attrs(kwargs)
        return one

    @classmethod
    def delete_by_id(cls, id_):
        one = cls.query.get_or_404(id_)
        with one.auto_commit():
            db.session.delete(one)

    def delete(self):
        with self.auto_commit():
            db.session.delete(self)

    def update(self, attrs: dict = None, **kwargs):
        with self.auto_commit():
            self.set_attrs(attrs)
            self.set_attrs(kwargs)
            db.session.add(self)

    @classmethod
    def update_by_id(cls, id_, attrs: dict = None, **kwargs):
        one = cls.query.get_or_404(id_)
        with one.auto_commit():
            one.set_attrs(attrs)
            one.set_attrs(kwargs)
            db.session.add(one)

    @classmethod
    def search(cls, **kwargs):
        pass

    # 获取表的记录数
    @classmethod
    def total(cls):
        return cls.query.count()

    def set_attrs(self, attrs: dict):
        if not attrs:
            return
        for key, value in attrs.items():
            if hasattr(self, key) and key not in self.blacklist:
                setattr(self, key, value)
