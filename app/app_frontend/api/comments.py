from flask import request

from app.model.db import Comment, Post
from app.model.view import CommentsQueryView
from app.utils import generate_res
from .blueprint import api
from ..validate import CommentValidate
from ..view_model import CommentsView
from ..view_model import IdView


@api.route('/comments/<int:pid>', methods=['GET', 'POST'])
def comments_view(pid):
    if request.method == 'POST':
        form = CommentValidate().validate_api()
        comment = Comment.update_comment(**form.data, post_id=pid)
        return generate_res(data=IdView(comment))
    query = CommentsQueryView()
    query_ = Comment.visibility().union(Post.search_by(id=pid).comments_.filter_by(show=True))
    pagination = Comment.paging_search(**query.search_parameter, query=query_)
    return generate_res(data=CommentsView(pagination.items, query.page))
