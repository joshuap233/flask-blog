from flask import request, current_app, send_from_directory

from app.model.db import Post
from app.model.view_model import PostView
from app.utils import generate_res, filters_filename
from app.validate.validate import PostValidate
from .blueprint import admin
from app.token_manager import login_required


@admin.route('/posts/post', methods=['POST', 'GET', 'PUT', 'DELETE'])
@login_required
def post_view():
    # 添加文章
    if request.method == 'POST':
        post = Post.create()
        return generate_res(data={'id': post.id})
    elif request.method == 'PUT':
        form = PostValidate().validate_api()
        Post.update_by_id(form.id.data, form.data)
        return generate_res()
    elif request.method == 'DELETE':
        Post.delete_by_id(request.get_json().get('id'))
        return generate_res()
    post = Post.query.get_or_404(request.args.get('id'))
    return generate_res(data=PostView(post))


# TODO: 多张图片上传,同时发送多张图片
@admin.route('/avatar', methods=['POST', 'GET', 'DELETE', 'PUT'])
@login_required
def avatar_view():
    import os
    path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'posts')
    if request.method == 'POST':
        post_id = request.form.get('id')
        img = request.files.get('image')
        filename = filters_filename(img.filename)
        img.save(os.path.join(path, filename))
        Post.update_by_id(post_id, {'links': filename})
        return generate_res()
    picture = request.args.get('picture')
    return send_from_directory(path, picture)
