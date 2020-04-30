from abc import ABCMeta, abstractmethod


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
