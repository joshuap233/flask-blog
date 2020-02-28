from flask import request, current_app, send_from_directory

from app.exception import RepeatException
from app.model.db import Tag
from app.model.view_model import TagsView, QueryView
from app.utils import generate_res, filters_filename
from app.validate.validate import TagValidate
from .blueprint import admin
from app.token_manager import login_required


# 获取所有标签,仅包含标签名
@admin.route('/posts/tags')
@login_required
def all_tags_view():
    return generate_res(data=[
        tag.name for tag in Tag.query.all()
    ])


# 获取所有标签,包含标签以及详细信息
@admin.route('/tags', methods=['POST', 'GET', 'DELETE', 'PUT'])
@login_required
def tags_view():
    if request.method == 'POST':
        tag = Tag.create()
        return generate_res(data={'id': tag.id})
    elif request.method == 'PUT':
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
    query = QueryView()
    pagination = Tag.search(**query.search_parameter)
    return generate_res(data=TagsView(pagination.items, query.page))


# TODO :同时发送多张图片
@admin.route('/tags/images/', methods=['POST', 'GET', 'DELETE', 'PUT'])
@login_required
def tags_pic_view():
    import os
    path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'tags')
    if request.method == 'POST':
        # TODO: 文件校验(svg过滤,压缩处理
        tag_id = request.form.get('id')
        img = request.files.get('image')
        filename = filters_filename(img.filename)
        img.save(os.path.join(path, filename))
        Tag.update_by_id(tag_id, picture=filename)
        return generate_res()
    picture = request.args.get('picture')
    return send_from_directory(path, picture)
