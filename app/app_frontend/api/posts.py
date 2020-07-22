from app.utils import generate_res
from .blueprint import api
from app.model.db import Post, Tag
from app.app_frontend.view_model import PostsView
from ..view_model import PostsQueryView
from app.model.baseDB import Visibility


@api.route('/posts')
def posts_view():
    query = PostsQueryView()
    query_ = Post.visibility_posts()
    posts = Post.paging_search(**query.search_parameter, query=query_)
    return generate_res(data=PostsView(posts.items, query.page))


def posts_search_view():
    pass


@api.route('/tag/<int:tid>/posts')
def posts_query_by_tags_view(tid):
    query = PostsQueryView()
    query_ = Tag.search_by(id=tid).posts.filter_by(visibility=Visibility.public.value)
    posts = Post.paging_search(**query.search_parameter, query=query_)
    return generate_res(data=PostsView(posts.items, query.page))
