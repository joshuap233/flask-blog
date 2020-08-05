from app.api_limiter import limiter
from app.email_manager import send_new_comments_email
from app.model.db import Comment, Post
from app.model.view import CommentsQueryView
from app.utils import generate_res
from .blueprint import api
from ..validate import CommentValidate
from ..view_model import CommentsView
from ..view_model import IdView


@api.route('/comments/<int:pid>')
def comments_view(pid):
    query = CommentsQueryView()
    query_ = Post.search_by(id=pid).comments_.filter_by(show=True)
    pagination = Comment.paging_search(**query.search_parameter, query=query_)
    return generate_res(data=CommentsView(pagination.items, query.page))


# TODO:小博客没多少评论,就先这样吧23333 20/hour
@api.route('/comments/<int:pid>', methods=['POST'])
@limiter.limit('20/hour')
def comments_post_view(pid):
    form = CommentValidate().validate_api()
    comment = Comment.update_comment(**form.data, post_id=pid)
    send_new_comments_email(form.content.data)
    return generate_res(data=IdView(comment))
