from app.model.db import Post
from app.app_admin.view_model import PostsView, PostView, IdView
from app.model.view import QueryView
from app.utils import generate_res, save_base64_img
from .blueprint import admin
from ..token_manager import login_required
from ..validate.validate import PostValidate, DeleteValidate
from flask import request
from app.cache import cache


@admin.route('/posts', defaults={'pid': -1}, methods=['POST', 'DELETE'])
@admin.route('/posts/<int:pid>', methods=['GET', 'PUT'])
@login_required
def post_view(pid):
    # 添加文章
    if request.method == 'POST':
        post = Post.create()
        return generate_res(data=IdView(post))
    elif request.method == 'PUT':
        form = PostValidate().validate_api()
        form.illustration.data = save_base64_img(form.illustration.data)
        cache.delete_many(f'view//api/post/{pid}', 'view//api/posts', 'view//api/tags')
        Post.update_by_id(pid, **form.data)
        return generate_res()
    elif request.method == 'DELETE':
        cache.delete_many('view//api/posts', 'view//api/tags')
        form = DeleteValidate().validate_api()
        for identify in form.id_list.data:
            Post.delete_by(id=identify)
        return generate_res()
    post = Post.search_by(id=pid)
    return generate_res(data=PostView(post))


@admin.route("/posts")
@login_required
def posts_view():
    query = QueryView()
    pagination = Post.paging_search(**query.search_parameter)
    return generate_res(data=PostsView(pagination.items, query.page))
