import os

from flask import request, current_app, send_from_directory

from .blueprint import api
from ..database import Post, Tag, User
from ..utils import required_login, generate_res, get_attr


@api.route('/admin/posts/<int:timesStamp>')
@required_login
def admin_write(timesStamp):
    post = Post.query.filter_by(date=timesStamp).first()
    return generate_res('success', 'get post', contents=post.contents, title=post.title, tags=post.tags)


@api.route('/admin/post/', methods=['POST'])
@api.route('/admin/posts/images/<string:timeStamp>/<string:filename>', methods=['GET'])
@required_login
def admin_images(timeStamp=None, filename=None):
    if request.method == 'POST':
        images = request.files.getlist('images')
        date = request.form.get('timeStamp')
        if images:
            path = os.path.join(current_app.config['UPLOAD_FOLDER'], date)
            os.mkdir(path) if not os.path.exists(path) else None
            [image.save(os.path.join(path, image.filename)) for image in images]
            return generate_res('success', 'image upload')
        else:
            return generate_res('failed', 'image empty')
    return send_from_directory(current_app.config['UPLOAD_FOLDER'] + timeStamp, filename)


@api.route('/admin/posts/', methods=['GET', 'POST', 'PUT'])
@required_login
def admin_posts():
    if request.method == 'POST':
        # 添加新文章
        data = request.get_json()
        date = data.get('timeStamp')
        post = Post(date, '', date)
        post.auto_commit()
        return generate_res('success', 'new post')
    elif request.method == 'PUT':
        try:
            data = request.get_json()
            title = data.get('title')
            if not title or Post.query.filter_by(title=title).first():
                return generate_res('failed', 'title empty or repetitive')
        except AttributeError as e:
            return generate_res('failed', e)
        date, tags = get_attr(['timeStamp', 'tags'], data)
        post = Post.query.filter_by(date=date).first()
        if not post:
            return generate_res('failed', 'post not found')
        post.set_attrs(data)
        [post.tags.append(Tag.query.filter_by(tag_name=tag).first() or Tag(tag)) for tag in tags]
        post.auto_commit()
        return generate_res('success', 'add posts')
    return generate_res('success', 'get post')


@api.route('/admin/auth/register/', methods=['POST'])
def admin_register():
    data = request.get_json()
    if data.get('phone'):
        data['phone'] = str(data['phone'])
    username, nickname, password = get_attr(['username', 'nickname', 'password'], data)
    if username and password and nickname:
        user = User()
        user.set_attrs(data)
        user.generate_password_hash(password)
        user.auto_commit()
        return generate_res('success', 'sign in')
    return generate_res('failed', 'empty password or username')


@api.route('/admin/auth/login/', methods=['POST'])
def admin_login():
    data = request.get_json()
    username, password = get_attr(['username', 'password'], data)
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        user.is_active = True
        user.auto_commit()
        return generate_res('success', 'login', id=user.id, token=user.generate_token(), expiration=3600)
    return generate_res('failed', 'login')


@api.route('/admin/auth/logout')
@required_login
def admin_logout():
    uid = request.get_json().get('id')
    user = User.query.filter_by(id=uid)
    user.is_active = False
    user.auto_commit()
    return generate_res('success', 'logout')
