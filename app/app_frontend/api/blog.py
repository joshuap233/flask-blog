from .blueprint import api
from app.model.db import Blog
from app.utils import generate_res
from app.model.view import BlogQueryView
from app.model.view import BlogsView


@api.route('/blog')
def blog_view():
    query = BlogQueryView()
    pagination = Blog.paging_search(**query.search_parameter)
    return generate_res(data=BlogsView(pagination.items, query.page))
