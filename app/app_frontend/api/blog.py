from .blueprint import api
from app.model.db import Blog
from app.utils import generate_res
from app.model.view import BaseQueryView, BlogsView


@api.route('/blog')
def blog_view():
    query = BaseQueryView()
    pagination = Blog.paging_search(**query.search_parameter)
    return generate_res(data=BlogsView(pagination.items, query.page))
