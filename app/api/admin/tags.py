from flask import request

from app.exception import RepeatException
from app.model.db import Tag
from app.model.view_model import TagsToJsonView, QueryView, JsonToTagView
from app.utils import generate_res, login_required
from .blueprint import admin


# 获取所有标签,仅包含标签名
@admin.route('/posts/tags')
@login_required
def all_tags_view():
    tags = [tag.name for tag in Tag.query.all()]
    return generate_res('success', data=tags)


# 获取所有标签,包含标签以及详细信息
@admin.route('/tags', methods=['POST', 'GET', 'DELETE', 'PUT'])
@login_required
def tags_view():
    if request.method == 'GET':
        query = QueryView(request.args)
        Tag.search()
        if query.search:
            # TODO: 暂时只支持按标签名查找
            pagination = Tag.query.filter(
                Tag.name.like(query.search)).order_by(
                query.orderBy).paginate(
                page=query.page, per_page=query.pageSize, error_out=False)
            return generate_res('success', data=TagsToJsonView(pagination.items, query.page))
        pagination = Tag.query.paginate(page=query.page, per_page=query.pageSize, error_out=False)
        tags = pagination.items
        return generate_res('success', data=TagsToJsonView(tags, query.page))
    new_tag = JsonToTagView(request.get_json())
    if request.method == 'PUT':
        tag = Tag.query.get_or_404(new_tag.id)
        # 如果修改了标签名,且修改后的标签名已存在
        if tag.name != new_tag.name and Tag.query.filter_by(name=new_tag.name).first():
            raise RepeatException(msg='标签名已存在')
        with tag.auto_add():
            tag.set_attrs(new_tag.__dict__)
        return generate_res('success')
    elif request.method == 'DELETE':
        tag = Tag.query.get_or_404(new_tag.id)
        tag.delete()
        return generate_res('success')
    elif request.method == 'POST':
        if Tag.query.filter_by(name=new_tag.name).first():
            raise RepeatException('标签已存在')
        tag = Tag()
        with tag.auto_add():
            tag.set_attrs(new_tag.__dict__)
            tag.count = 1
        return generate_res('success')
