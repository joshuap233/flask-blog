import os

from flask import jsonify, request, current_app, send_from_directory
from flask_login import login_required, logout_user, login_user

from .blueprint import api
from ..database import Post, Tag, db, User


@api.route('/admin/posts/<int:timesStamp>')
@login_required
def admin_write(timesStamp):
    post = Post.query.filter_by(post_date=timesStamp).first()
    return jsonify({
        "contents": post.post_contents,
        "title": post.post_title,
        "tags": post.tags
    })


@api.route('/admin/post/', methods=['POST'])
@api.route('/admin/posts/images/<string:timeStamp>/<string:filename>', methods=['GET'])
@login_required
def admin_images(timeStamp=None, filename=None):
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
                'msg': 'image empty'
            })
    return send_from_directory(current_app.config['UPLOAD_FOLDER'] + timeStamp, filename)


@api.route('/admin/posts/', methods=['GET', 'POST', 'PUT'])
@login_required
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
                    "msg": "title empty or repetitive"
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
                "msg": 'post not found'
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
            "msg": "add posts"
        })
    return jsonify({
        "state": "success",
        "msg": 'get post'
    })


@api.route('/admin/auth/register', methods=['POST'])
def auth():
    data = request.get_json()
    username = data.get('username')
    nickname = data.get('nickname')
    email = data.get('email')
    phone = str(data.get('phone'))
    password = data.get('password')
    if username and password and nickname:
        user = User(username=username, nickname=nickname, phone=phone, email=email)
        user.generate_password_hash(password)
        db.session.add(user)
        db.session.commit()
        return jsonify({
            'state': 'success',
            'msg': 'sign in'
        })
    return jsonify({
        'state': 'failed',
        'msg': 'empty password or username'
    })


@api.route('/admin/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        login_user(user)
        return jsonify({
            'status': 'success',
            'msg': 'login'
        })
    return jsonify({
        'status': 'failed',
        'msg': 'login'
    })


@api.route('/admin/auth/logout')
@login_required
def logout():
    logout_user()
    return jsonify({
        'status': 'success',
        'msg': 'logout'
    })
