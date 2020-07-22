from flask import request

from app.app_admin.validate import DeleteComment, CheckComment
from app.model.baseDB import CommentEnum
from app.model.db import Comment, CommentReply
from app.model.view import BaseQueryView, CommentsQueryView
from app.utils import generate_res
from .blueprint import admin
from ..token_manager import login_required
from ..view_model import CommentsView, RepliesView


@admin.route('/comments', methods=['DELETE', 'PUT', 'GET'])
@login_required
def comments_view():
    if request.method == 'DELETE':
        # TODO:批量删除,
        form = DeleteComment().validate_api()
        modal = Comment if form.type.data == CommentEnum.comment.value else CommentReply
        modal.delete_by(id=form.id.data)
        return generate_res()
    # 审核评论,TODO,添加配置,设置评论是否需要审核
    if request.method == 'PUT':
        form = CheckComment().validate_api()
        modal = Comment if form.type.data == CommentEnum.comment.value else CommentReply
        modal.update_by_id(form.id.data, **form.data)
        return generate_res()
    query = CommentsQueryView()
    pagination = Comment.paging_search(**query.search_parameter)
    return generate_res(data=CommentsView(pagination.items, query.page))


@admin.route('/replay')
@login_required
def reply_view():
    query = BaseQueryView()
    pagination = CommentReply.paging_search(**query.search_parameter)
    return generate_res(data=RepliesView(pagination.items, query.page))
