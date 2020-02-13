from flask import request

from app.model.db import Post
from app.utils import generate_res
from .blueprint import api


@api.route('/post')
def post_view():
    post = Post.query.get_or_404(request.args.get('id'))
    return generate_res(data={
        'id': post.id,
        'title': post.title,
        'article': post.article
    })
