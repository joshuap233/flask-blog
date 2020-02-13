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


class Base(db.Model):
    __abstract__ = True
    blacklist = []

    def update(self, attrs):
        with self.auto_commit():
            self.set_attrs(attrs)
            db.session.add(self)

    def delete(self):
        with self.auto_commit():
            db.session.delete(self)

    @classmethod
    def create(cls, attrs=None):
        one = cls()
        with one.auto_commit():
            if attrs:
                one.set_attrs(attrs)
        return one

    # 获取表的记录数
    @classmethod
    def total(cls):
        return cls.query.count()

    def set_attrs(self, attrs: dict):
        for key, value in attrs.items():
            if hasattr(self, key) and key not in self.blacklist:
                setattr(self, key, value)
