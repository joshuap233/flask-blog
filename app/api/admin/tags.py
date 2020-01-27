from flask import request

from .blueprint import admin
from app.database import Tag
from app.utils import generate_res, required_login


# 获取所有标签,仅包含标签名
@admin.route('/posts/tags/')
@required_login
def all_tags_view():
    tags = [tag.name for tag in Tag.query.all()]
    return generate_res('success', '', data=tags)


# 获取所有标签,包含标签以及详细信息
@admin.route('/tags/', methods=['POST', 'GET', 'DELETE', 'PUT'])
@required_login
def tags_view():
    data = request.get_json()
    if request.method == 'PUT':
        tag_id = data.get('tagId')
        tag = Tag.query.get(tag_id)
        if not tag:
            return generate_res('failed', ''), 404
        else:
            tag.describe = data['describe']
            tag.name = data['name']
            tag.auto_add()
            return generate_res('success', '')
    elif request.method == 'DELETE':
        tag_id = request.get_json().get('tagId')
        tag = Tag.query.get(tag_id)
        if not tag:
            return generate_res('failed', ''), 404
        tag.auto_delete()
        return generate_res('success', '')
    elif request.method == 'POST':
        if Tag.quary.filter_by(data['name']):
            return generate_res('failed', '标签已存在')
        tag = Tag(name=data['name'], describe=data['describe'])
        tag.auto_add()
        return generate_res('success', '')
    order_by = request.args.get('orderBy')
    if order_by:
        pass
    search = request.args.get('search')
    if search:
        pass
    page = int(request.args.get('page'))
    page_size = int(request.args.get('pageSize'))
    pagination = Tag.query.paginate(page=page, page_size=page_size, error_out=False)
    tags = pagination.items
    if not tags:
        return generate_res('failed', 'page not found'), 404
    tags = [{'tagId': tag.id, 'name': tag.name, 'describe': tag.describe, 'count': tag.count} for tag in tags]
    generate_res('success', '', data={
        'total': 20,
        'page': page,
        'tags': tags
    })
