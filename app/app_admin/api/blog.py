from .blueprint import admin
from ..token_manager import login_required
from flask import request
from app.model.db import Blog
from app.utils import generate_res
from ..validate.validate import ModifyBlog
from app.model.view import BlogQueryView
from ..view_model import BlogsView


@admin.route('/blog/<int:bid>', methods=['DELETE'])
@admin.route('/blog', defaults={'tid': -1}, methods=['PUT', 'GET'])
@login_required
def blog_view(bid):
    if request.method == 'DELETE':
        Blog.delete_by(id=bid)
        return generate_res()
    if request.method == 'PUT':
        form = ModifyBlog().validate_api()
        Blog.update_by_id(id=form.id.data, **form.data)
        return generate_res()
    query = BlogQueryView()
    pagination = Blog.paging_search(**query.search_parameter)
    return generate_res(data=BlogsView(pagination.items, query.page))
