from flask import request

from app.model.db import Post, db, Tag
from app.model.view_model import PostToJsonView, JsonToPostView
from app.utils import generate_res, login_required
from .blueprint import admin


@admin.route('/posts/post/', methods=['POST', 'GET', 'PUT', 'DELETE'])
@login_required
def post_view():
    new_post = JsonToPostView(request.get_json())
    # 添加文章
    if request.method == 'POST':
        post = Post()
        post.auto_add()
        return generate_res('success', data={
            'postId': post.id
        })
    elif request.method == 'PUT':
        if not new_post.id:
            return generate_res("failed"), 404
        post = Post.query.get(new_post.id)
        post.set_attrs(new_post.__dict__)
        for tag in new_post.tags:
            tag = Tag.query.filter_by(name=tag).first() or Tag(name=tag)
            # TODO: 对象对比???可能报错
            if tag in post.tags:
                continue
            post.tags.append(tag)
            tag.count = tag.count + 1
        post.auto_add()
        return generate_res('success')
    elif request.method == 'DELETE':
        try:
            post = Post.query.get(new_post.id)
            db.session.delete(post)
            db.session.commit()
            return generate_res('success')
        except Exception as e:
            print(e)
            return generate_res('failed'), 404
    post = Post.query.get(new_post.id)
    return generate_res('success', data=PostToJsonView(post).__dict__) if post else generate_res('failed'), 404
