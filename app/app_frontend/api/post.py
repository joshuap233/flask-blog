from flask import request

from app.model.db import Post
from app.utils import generate_res
from .blueprint import api
from app.app_frontend.view_model import PostView
from app.app_frontend.cache import cache


@api.route('/post')
@cache.cached()
def post_view():
    post = Post.search_by(id=request.args.get('id'))
    return generate_res(data=PostView(post))
