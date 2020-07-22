from flask import request

from app.app_admin.validate import DeleteCommentValidate, CommentValidate
from app.model.db import Comment
from app.model.view import CommentsQueryView
from app.utils import generate_res
from .blueprint import admin
from ..token_manager import login_required
from ..view_model import CommentsView


@admin.route('/comments/<int:cid>', methods=['PUT'])
@admin.route('/comments', defaults={'cid': -1}, methods=['DELETE', 'GET'])
@login_required
def comments_view(cid):
    if request.method == 'DELETE':
        form = DeleteCommentValidate().validate_api()
        Comment.delete_all_by_id(form.id_list.data)
        return generate_res()
    # 审核评论,TODO,添加配置,设置评论(默认)是否需要审核
    if request.method == 'PUT':
        form = CommentValidate().validate_api()
        Comment.update_by_id(cid, **form.data)
        return generate_res()
    query = CommentsQueryView()
    pagination = Comment.paging_search(**query.search_parameter)
    return generate_res(data=CommentsView(pagination.items, query.page))
