from flask import request

from app.model.db import Post
from app.model.view_model import PostsView, QueryView
from app.utils import generate_res, login_required
from .blueprint import admin


@admin.route("/posts")
@login_required
def posts_view():
    query = QueryView(request.args)
    pagination = Post.search(
        search=query.search,
        order_by=query.orderBy,
        page=query.page,
        per_page=query.pageSize
    )
    return generate_res(data=PostsView(pagination.items, query.page))
