from .blueprint import api
from app.utils import generate_res
from app.model.view import CommentQueryView, ReplyQueryView
from ..view_model import CommentsView, RepliesView
from flask import request
from ..view_model import IdView
from ..validate import CommentValidate
from app.model.db import Comment, CommentReply


@api.route('/comments', methods=['GET', 'POST'])
def comments_view():
    if request.method == 'POST':
        form = CommentValidate().validate_api()
        com = Comment.update_comment(**form.data)
        return generate_res(data=IdView(com))
    query = CommentQueryView()
    pagination = Comment.paging_search(**query.search_parameter)
    return generate_res(data=CommentsView(pagination.items, query.page))


@api.route('/replay')
def reply_view():
    query = ReplyQueryView()
    pagination = CommentReply.paging_search(**query.search_parameter)
    return generate_res(data=RepliesView(pagination.items, query.page))
