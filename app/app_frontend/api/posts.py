from app.utils import generate_res
from .blueprint import api
from app.model.view import QueryView
from app.model.db import Post
from app.model.baseDB import Visibility
from app.app_frontend.view_model import PostsView


@api.route('/posts')
def posts_view():
    query = QueryView(order_by=False)
    tid = query.filters.get('tid')
    posts = Post.paging_by_tid(
        tid, **query.search_parameter,
        visibility=Visibility.public.value
    ) if tid else Post.paging_search(
        **query.search_parameter,
        visibility=Visibility.public.value
    )
    return generate_res(data=PostsView(posts.items, query.page))
