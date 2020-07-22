from .blueprint import admin
from ..token_manager import login_required
from flask import request
from app.model.db import Blog
from app.utils import generate_res
from app.app_admin.validate import ModifyBlog, DeleteBlog
from app.model.view import BaseQueryView, BlogsView
from ..view_model import IdView


@admin.route('/blog', methods=['PUT', 'GET', 'DELETE'])
@login_required
def blog_view():
    if request.method == 'DELETE':
        form = DeleteBlog().validate_api()
        Blog.delete_all_by_id(form.id_list.data)
        return generate_res()
    if request.method == 'PUT':
        form = ModifyBlog().validate_api()
        if form.isNew.data:
            blog = Blog.create(**form.data)
            return generate_res(data=IdView(blog))
        Blog.update_by_id(form.id.data, **form.data)
        return generate_res()
    query = BaseQueryView()
    pagination = Blog.paging_search(**query.search_parameter)
    return generate_res(data=BlogsView(pagination.items, query.page))
