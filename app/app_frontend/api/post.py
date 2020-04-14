from flask import request

from app.shared.model.db import Post
from app.utils import generate_res
from .blueprint import api


@api.route('/post')
def post_view():
    post = Post.search_by(id=request.args.get('id'))
    return generate_res(data={
        'id': post.id,
        'title': post.title,
        'article': post.article_html,
        'change_date': post.change_date,
        'comments': post.comments,
        'tags': [{
            'id': tag.id,
            'name': tag.name
        } for tag in post.tags]
    })
