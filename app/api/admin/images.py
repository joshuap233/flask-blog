import os

from flask import request, current_app, send_from_directory

from app.exception import NotFound
from app.model.db import Post, Link, Tag
from app.model.view_model import QueryView, ImagesView, ImageUrlView, NewImageView
from app.token_manager import login_required
from app.utils import generate_res, filters_filename
from app.validate.validate import DeleteValidate, ChangeImageValidate
from .blueprint import admin


# 图片上传
@admin.route('/images/<source>/<int:source_id>', methods=['POST'])
@login_required
def images_upload_view(source, source_id):
    if source == 'tags':
        model = Tag
    elif source == 'posts':
        model = Post
    else:
        raise NotFound()
    path = current_app.config['UPLOAD_FOLDER']
    # TODO: 文件校验(svg过滤,压缩处理
    img = request.files.get('image')
    filename = filters_filename(img)
    img.save(os.path.join(path, filename))
    model.update_by_id(source_id, links=filename)
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
            os.remove(os.path.join(current_app.config['UPLOAD_FOLDER'], link.url))
            link.delete()
        return generate_res()
    elif request.method == 'PUT':
        form = ChangeImageValidate().validate_api()
        print(form)
        Link.update_by_id(image_id, **form.data)
        return generate_res()
    elif request.method == 'POST':
        path = current_app.config['UPLOAD_FOLDER']
        # images = request.files.getlist('image)
        img = request.files.get('image')
        filename = filters_filename(img)
        img.save(os.path.join(path, filename))
        link = Link.create(url=filename)
        return generate_res(data=NewImageView(link))
    query = QueryView()
    pagination = Link.paging_search(**query.search_parameter)
    return generate_res(data=ImagesView(pagination.items, query.page))
