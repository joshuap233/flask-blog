from flask import request

from app.model.db import Post, Tag
from app.model.view_model import PostToJsonView, JsonToPostView
from app.utils import generate_res, login_required
from .blueprint import admin


@admin.route('/posts/post', methods=['POST', 'GET', 'PUT', 'DELETE'])
@login_required
def post_view():
    # 添加文章
    if request.method == 'POST':
        post = Post.create(commit=True)
        return generate_res('success', data={'postId': post.id})
    elif request.method == 'PUT':
        new_post = JsonToPostView(request.get_json())
        if not new_post.id:
            return generate_res("failed"), 404
        post = Post.query.get_or_404(new_post.id)

        with post.auto_add():
            post.set_attrs(new_post.__dict__)
            for tag in new_post.tags:
                # TODO
                tag = Tag.query.filter_by(name=tag).first() or Tag(name=tag)
                if tag in post.tags:
                    continue
                post.tags.append(tag)
                tag.count = tag.count + 1
        return generate_res('success')
    elif request.method == 'DELETE':
        new_post = JsonToPostView(request.get_json())
        post = Post.query.get_or_404(new_post.id)
        tags = post.tags
        for tag in tags:
            tag.count -= 1
        post.delete()
        return generate_res('success')
    post = Post.query.get_or_404(request.args.get('postId'))
    return generate_res('success', data=PostToJsonView(post))
