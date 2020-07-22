from app.model.db import Post
from app.model.view import BaseQueryView
from app.utils import generate_res
from .blueprint import api
from ..view_model import ArchiveView


@api.route('/archive')
def archive():
    query = BaseQueryView()
    visibility_posts = Post.visibility_posts()
    pagination = Post.paging_search(**query.search_parameter, query=visibility_posts)
    return generate_res(data=ArchiveView(pagination.items, query.page))


@api.route('/test/comments', methods=['POST'])
def view_test123():
    return generate_res()
