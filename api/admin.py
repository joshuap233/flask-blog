import os

from flask import jsonify, request, current_app

from .blueprint import api
from ..database import Post, Tag, db


@api.route('/admin/posts/<int:timesStamp>')
def admin_write(timesStamp):
    post = Post.query.filter_by(post_date=timesStamp).first()
    return jsonify({
        "contents": post.post_contents,
        "title": post.post_title,
        "tags": post.tags
    })


@api.route('/admin/posts/images/', methods=['POST', 'GET'])
def admin_images():
    if request.method == 'POST':
        images = request.files.getlist('images')
        date = request.form.get('timeStamp')

        if images:
            path = os.path.join(current_app.config['UPLOAD_FOLDER'], date)
            os.mkdir(path) if not os.path.exists(path) else None
            [image.save(os.path.join(path, image.filename)) for image in images]
            return jsonify({
                'status': 'success',
                'msg': 'image upload'
            })
        else:
            return jsonify({
                'status': 'failed',
                'msg': '图片为空'
            })


@api.route('/admin/posts/', methods=['GET', 'POST', 'PUT'])
def admin_posts():
    if request.method == 'POST':
        # 添加新文章
        data = request.get_json()
        date = data.get('timeStamp')
        post = Post(date, '', date)
        db.session.add(post)
        db.session.commit()
        return jsonify({
            'status': 'success',
            'mgs': 'new post'
        })
    elif request.method == 'PUT':
        try:
            data = request.get_json()
            title = data.get('title')
            if not title or Post.query.filter_by(post_title=title).first():
                return jsonify({
                    "status": "failed",
                    "msg": "标题不能重复或为空"
                })
        except AttributeError as e:
            return jsonify({
                "status": "failed",
                "msg": e
            })

        date = data.get('timeStamp')
        contents = data.get('contents')
        tags = data.get('tags')
        publish = data.get('publish') == 'true'
        post = Post.query.filter_by(post_date=date).first()
        if not post:
            return jsonify({
                'state': 'failed',
                "msg": '文章不存在'
            })
        post.post_title = title
        post.post_contents = contents
        post.post_date = date
        post.post_publish = publish
        [post.tags.append(Tag.query.filter_by(tag_name=tag).first() or Tag(tag)) for tag in tags]
        db.session.add(post)
        db.session.commit()
        return jsonify({
            "state": "success",
            "msg": "add posts success"
        })
    return jsonify({
        "state": "success",
        "msg": 'get success'
    })
