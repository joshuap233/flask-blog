import os

from app.model.db import Post
from app.model.view_model import PostsView, QueryView, PostView, IdView
from app.utils import generate_res
from .blueprint import admin
from app.token_manager import login_required
from app.validate.validate import PostValidate, DeleteValidate
from flask import request


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
        Post.update_by_id(pid, **form.data)
        return generate_res()
    elif request.method == 'DELETE':
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
