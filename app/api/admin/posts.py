from app.model.db import Post
from app.model.view_model import PostsView, QueryView
from app.utils import generate_res
from .blueprint import admin
from app.token_manager import login_required


@admin.route("/posts")
@login_required
def posts_view():
    query = QueryView()
    pagination = Post.search(**query.search_parameter)
    return generate_res(data=PostsView(pagination.items, query.page))
