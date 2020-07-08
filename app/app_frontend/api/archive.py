from app.model.db import Post
from app.model.view import ArchiveQueryView
from app.utils import generate_res
from .blueprint import api
from ..view_model import ArchiveView


@api.route('/archive')
def archive():
    query = ArchiveQueryView()
    pagination = Post.search(**query.search_parameter)
    return generate_res(data=ArchiveView(pagination.items, query.page))
