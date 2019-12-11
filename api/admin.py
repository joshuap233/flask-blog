import os

from flask import jsonify, request, current_app

from .blueprint import api
from ..database import Post, Tag, db


@api.route('/admin/posts/', methods=['GET', 'POST'])
def admin_post():
    if request.method == 'POST':
        try:
            data = request.form
            if data:
                pass
            images = request.files.getlist('images')
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
        path = os.path.join(current_app.config['UPLOAD_FOLDER'], title)
        os.mkdir(path) if not os.path.exists(path) else None
        for image in images:
            image.save(os.path.join(path, image.filename))
        date = data.get('timeStamp')
        contents = data.get('contents')
        tags = data.get('tags').split(',')
        publish = data.get('publish') == 'true'
        post = Post(title, contents, date, publish)
        [post.tags.append(Tag.query.filter(Tag.tag_name == tag).first() or Tag(tag)) for tag in tags]
        db.session.add(post)
        db.session.commit()
        return jsonify({
            "msg": "post success"
        })
    return jsonify({
        "msg": "post success"
    })
