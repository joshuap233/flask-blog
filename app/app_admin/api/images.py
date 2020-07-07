import os

from flask import request, current_app, send_from_directory

from app.exception import NotFound
from app.model.db import Post, Link, Tag
from app.app_admin.view_model import ImagesView, ImageUrlView, NewImageView
from app.model.view import QueryView
from app.utils import generate_res, save_img, security_remove_file
from .blueprint import admin
from ..token_manager import login_required
from ..validate.validate import DeleteValidate, ChangeImageValidate


# 图片上传
@admin.route('/images/<source>/<int:source_id>', methods=['POST'])
@login_required
def images_upload_view(source, source_id):
    if source not in ['posts', 'tags']:
        raise NotFound()
    filename = save_img()
    if source == 'tags':
        Tag.update_by_id(source_id, link=filename)
    elif source == 'posts':
        Post.update_by_id(source_id, links=filename)
    return generate_res(data=ImageUrlView(filename))


@admin.route('/images/image/<filename>')
def send_images_view(filename):
    path = current_app.config['UPLOAD_FOLDER']
    return send_from_directory(path, filename)


# 图片信息获取,修改(添加描述),删除
@admin.route('/images', defaults={'image_id': -1}, methods=['GET', 'DELETE', 'POST'])
@admin.route('/images/<image_id>', methods=['PUT'])
@login_required
def images_query_view(image_id):
    if request.method == 'DELETE':
        form = DeleteValidate().validate_api()
        for identify in form.id_list.data:
            link = Link.search_by(id=identify)
            security_remove_file(link.url)
            link.delete()
        return generate_res()
    elif request.method == 'PUT':
        form = ChangeImageValidate().validate_api()
        Link.update_by_id(image_id, **form.data)
        return generate_res()
    elif request.method == 'POST':
        filename = save_img()
        link = Link.create(url=filename)
        return generate_res(data=NewImageView(link))
    query = QueryView()
    pagination = Link.paging_search(**query.search_parameter)
    return generate_res(data=ImagesView(pagination.items, query.page))
