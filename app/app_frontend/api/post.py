from flask import request

from app.model.db import Post
from app.utils import generate_res
from .blueprint import api
from app.app_frontend.view_model import PostView
from app.cache import cache


def make_cache_key():
    return f'view//api/post/{request.args.get("id")}'


@api.route('/post')
@cache.cached(make_cache_key=make_cache_key)
def post_view():
    post = Post.search_by(id=request.args.get('id'))
    return generate_res(data=PostView(post))
