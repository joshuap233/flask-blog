from flask import request

from app.model.db import Tag
from app.model.view_model import TagsToJsonView, QueryView, JsonToTagView
from app.utils import generate_res, login_required
from .blueprint import admin


# 获取所有标签,仅包含标签名
@admin.route('/posts/tags/')
@login_required
def all_tags_view():
    tags = [tag.name for tag in Tag.query.all()]
    return generate_res('success', '', data=tags)


# 获取所有标签,包含标签以及详细信息
@admin.route('/tags/', methods=['POST', 'GET', 'DELETE', 'PUT'])
@login_required
def tags_view():
    query = QueryView(request.args)
    new_tag = JsonToTagView(request.get_json())
    if request.method == 'PUT':
        tag = Tag.query.get(new_tag.id)
        if not tag:
            return generate_res('failed', ''), 404
        tag.set_attrs(new_tag.__dict__)
        tag.auto_add()
        return generate_res('success', '')
    elif request.method == 'DELETE':
        tag = Tag.query.get(new_tag.id)
        if not tag:
            return generate_res('failed', ''), 404
        tag.auto_delete()
        return generate_res('success', '')
    elif request.method == 'POST':
        if Tag.quary.filter_by(new_tag.name):
            return generate_res('failed', '标签已存在')
        tag = Tag()
        tag.set_attrs(new_tag.__dict__)
        tag.auto_add()
        return generate_res('success', '')
    if query.search:
        # TODO: 暂时只支持按标签名查找
        pagination = Tag.query.filter(
            Tag.name.like(query.search)).order_by(
            query.orderBy).paginate(
            page=query.page, per_page=query.pageSize, error_out=False)
        return generate_res('success', '', data={
            'total': Tag.total(),
            'page': query.page,
            'tags': TagsToJsonView(pagination.items).fill()
        })
    pagination = Tag.query.paginate(page=query.page, page_size=query.pageSize, error_out=False)
    tags = pagination.items
    return generate_res('failed', 'page not found'), 404 if not tags else generate_res('success', '', data={
        'total': Tag.total(),
        'page': query.page,
        'tags': TagsToJsonView(tags).fill()
    })
