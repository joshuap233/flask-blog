from flask import jsonify, request

from .blueprint import api
from ..database import Post, Tag, db


@api.route('/admin/posts/', methods=['GET', 'POST'])
def admin_post():
    if request.method == 'POST':
        try:
            data = request.get_json()
            date = data.get('timeStamp')
            title = data.get('title')
            contents = data.get('contents')
            tags = data.get('tags')
            publish = data.get('publish')
        except AttributeError as e:
            return jsonify({
                "status": "failed",
                "msg": e
            })

        if title and not Post.query.filter_by(post_title=title).first():
            tags_ = [Tag(tag) for tag in tags]
            post = Post(title, contents, date, publish, tags_)
            db.session.add_all(tags_)
            db.session.add(post)
            db.session.commit()
            return jsonify({
                "msg": "post success"
            })
        else:
            return jsonify({
                "status": "failed",
                "msg": "标题不能重复或为空"
            })

    return jsonify({
        "msg": "post success"
    })
