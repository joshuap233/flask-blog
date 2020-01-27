import time

from flask import request

from .blueprint import admin
from app.database import Post, db, Tag
from app.utils import generate_res, required_login


@admin.route('/posts/post/', methods=['POST', 'GET', 'PUT', 'DELETE'])
@required_login
def post_view():
    # 添加文章
    if request.method == 'POST':
        post = Post()
        post.auto_add()
        return generate_res('success', '', data={
            'postId': post.id
        })
    elif request.method == 'PUT':
        data = request.get_json()
        post_id = data.get('id')
        if not post_id:
            return generate_res("failed", ''), 404
        post = Post.query.get(data[post_id])
        data['create_data'] = time.mktime(time.strptime(data['createDate'], '%Y/%m/%d %H:%M'))
        data['change_date'] = time.mktime(time.strptime(data['changeDate'], '%Y/%m/%d %H:%M'))
        tags = []
        for tag in data['tags']:
            tag = Tag.query.filter_by(name=tag).first()
            if tag in post.tags:
                continue
            if not tag:
                tag = Tag(name=tag)
            tags.append(tag)
            tag.count = tag.count + 1
        post.tags.update(tags)
        post.auto_add()
        return generate_res('success', '')
    elif request.method == 'DELETE':
        try:
            post_id = request.get_json().get('postId')
            post = Post.query.get(post_id)
            db.session.delete(post)
            db.session.commit()
            return generate_res('success', '')
        except Exception as e:
            print(e)
            return generate_res('failed', ''), 404
    post_id = int(request.args.get('postId'))
    post = Post.query.get(post_id)
    if not post:
        return generate_res('failed', ''), 404
    data = {
        'postId': post['id'],
        'title': post['title'],
        'tags': [tag['name'] for tag in post.tags],
        'visibility': post['visibility'],
        'comments': time.strftime("%Y/%m/%d %H:%M", time.localtime(post['comments'])),
        'changeDate': time.strftime("%Y/%m/%d %H:%M", time.localtime(post['create_date']))
    }
    return generate_res('success', '', data=data)
