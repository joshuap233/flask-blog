from flask import request

from app.model.db import Post
from app.model.view_model import PostView
from app.utils import generate_res, login_required
from app.validate.validate import PostValidate
from .blueprint import admin


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
