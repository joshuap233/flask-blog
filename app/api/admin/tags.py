from flask import request

from app.exception import RepeatException
from app.model.db import Tag
from app.model.view_model import TagsView, QueryView
from app.utils import generate_res, login_required
from app.validate.validate import TagValidate
from .blueprint import admin


# 获取所有标签,仅包含标签名
@admin.route('/posts/tags')
@login_required
def all_tags_view():
    tags = [tag.name for tag in Tag.query.all()]
    return generate_res(data=tags)


# 获取所有标签,包含标签以及详细信息
@admin.route('/tags', methods=['POST', 'GET', 'DELETE', 'PUT'])
@login_required
def tags_view():
    if request.method == 'PUT':
        form = TagValidate().validate_api()
        tag = Tag.query.get_or_404(form.id.data)
        # 如果修改了标签名,且修改后的标签名已存在
        if tag.name != form.name.data and Tag.query.filter_by(name=form.name.data).first():
            raise RepeatException(msg='标签名已存在')
        tag.update(form.data)
        return generate_res()
    elif request.method == 'DELETE':
        Tag.delete_by_id(request.get_json().get('id'))
        return generate_res()
    elif request.method == 'POST':
        form = TagValidate().validate_api()
        if Tag.query.filter_by(name=form.name.data).first():
            raise RepeatException('标签已存在')
        Tag.create(form.data, count=1)
        return generate_res()
    query = QueryView(request.args)

    pagination = Tag.search(
        search=query.search,
        order_by=query.orderBy,
        page=query.page,
        per_page=query.pageSize
    )
    return generate_res(data=TagsView(pagination.items, query.page))
