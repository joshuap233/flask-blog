from flask import request

from app.model.db import Tag
from app.app_admin.view_model import TagsView, IdView, AllTagsView
from app.model.view import QueryView
from app.utils import generate_res
from ..validate.validate import TagValidate, DeleteValidate
from .blueprint import admin
from ..token_manager import login_required
from app.signals import cache_signals, SIGNAL_SENDER


# 获取所有标签,仅包含标签名
@admin.route('/posts/tags/all')
@login_required
def all_tags_view():
    return generate_res(data=AllTagsView().data)


# 获取所有标签,包含标签以及详细信息
@admin.route('/tags', defaults={'tid': -1}, methods=['POST', 'GET', 'DELETE'])
@admin.route('/tags/<int:tid>', methods=['PUT'])
@login_required
def tags_view(tid):
    if request.method == 'POST':
        tag = Tag.create()
        return generate_res(data=IdView(tag))
    elif request.method == 'PUT':
        form = TagValidate().validate_api()
        tag = Tag.search_by(id=tid)
        # 如果修改了标签名
        if tag.name != form.name.data:
            tag.check_repeat(name=form.name.data)
        tag.update(**form.data)
        cache_signals.send(SIGNAL_SENDER['modifyTags'])
        return generate_res()
    elif request.method == 'DELETE':
        form = DeleteValidate().validate_api()
        for identify in form.id_list.data:
            Tag.delete_by(id=identify)
        cache_signals.send(SIGNAL_SENDER['deleteTags'])
        return generate_res()
    query = QueryView()
    pagination = Tag.paging_search(**query.search_parameter)
    return generate_res(data=TagsView(pagination.items, query.page))
