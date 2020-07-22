from .blueprint import api
from app.utils import generate_res
from app.model.view import CommentsQueryView
from ..view_model import CommentsView, RepliesView
from flask import request
from ..view_model import IdView
from ..validate import CommentValidate
from app.model.db import Comment, CommentReply, Post


@api.route('/comments/<int:pid>', methods=['GET', 'POST'])
def comments_view(pid):
    if request.method == 'POST':
        form = CommentValidate().validate_api()
        com = Comment.update_comment(**form.data, post_id=pid)
        return generate_res(data=IdView(com))
    query = CommentsQueryView()
    pagination = Comment.paging_search(**query.search_parameter, query=Post.search_by(id=pid).comments_)
    return generate_res(data=CommentsView(pagination.items, query.page))


@api.route('/replay')
def reply_view():
    query = CommentsQueryView()
    pagination = CommentReply.paging_search(**query.search_parameter)
    return generate_res(data=RepliesView(pagination.items, query.page))
