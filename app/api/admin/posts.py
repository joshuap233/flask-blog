from flask import request

from app.model.db import Post
from app.model.view_model import PostsToJsonView, QueryView
from app.utils import generate_res, login_required
from .blueprint import admin


@admin.route("/posts")
@login_required
def posts_view():
    query = QueryView(request.args)
    if query.search:
        # TODO: 支持按日期...查找,暂时只支持按文章标题查找
        pagination = Post.query.filter(
            Post.title.like(query.search)).order_by(
            query.orderBy).paginate(page=query.page, per_page=query.pageSize, error_out=False)
        return generate_res('success', data={
            'total': Post.total(),
            'page': query.page,
            'post': PostsToJsonView(pagination.items)
        })
    pagination = Post.query.order_by(
        query.orderBy).paginate(
        page=query.page, per_page=query.pageSize, error_out=False)
    posts = pagination.items
    return generate_res('success', data={
        'total': Post.total(),
        'page': query.page,
        'post': PostsToJsonView(posts)
    })
