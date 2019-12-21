import os

from flask import request, current_app, send_from_directory

from .blueprint import api
from ..database import Post, Tag, User
from ..utils import required_login, generate_res, get_attr


@api.route('/admin/posts/images/', methods=['GET', 'PUT'])
@required_login
def admin_images():
    if request.method == 'PUT':
        images = request.files.getlist('images')
        pid = str(request.form.get('id'))
        if images:
            path = os.path.join(current_app.config['UPLOAD_FOLDER'], pid)
            os.mkdir(path) if not os.path.exists(path) else None
            [image.save(os.path.join(path, image.filename)) for image in images]
            return generate_res('success', 'image upload')
        else:
            return generate_res('failed', 'image empty')
    data = request.get_json()
    pid, filename = get_attr(['id', 'filename'], data)
    return send_from_directory(current_app.config['UPLOAD_FOLDER'] + str(pid), filename)


# TODO 分页
@api.route('/admin/posts/page/<int:page>')
@required_login
def admin_posts(page):
    pagination = Post.query.order_by(Post.create_date.desc()).paginate(page=page, per_page=15, error_out=False)
    posts = pagination.items
    data = []
    for post in posts:
        data.append({
            "id": post.id,
            "title": post.title,
            "create_date": post.create_date,
            "change_date": post.change_date,
            "tags": [tag.name for tag in post.tags],
            "publish": post.publish
        })
    return generate_res('success', 'get post', data=data)


@api.route('/admin/posts/', methods=['GET', 'POST', 'PUT'])
@required_login
def admin_post():
    data = request.get_json()
    if request.method == 'POST':
        # 添加新文章
        try:
            create_date = data.get('create_date')
        except AttributeError:
            return generate_res("failed", "empty create_date")
        post = Post(create_date=create_date)
        post.auto_commit()
        return generate_res('success', 'new post', id=post.id)
    elif request.method == 'PUT':
        try:
            # 前端生成空标签列表
            pid, tags = get_attr(['id', 'tags'], data)
        except AttributeError:
            return generate_res('failed', 'get post id and tags failed')
        post = Post.query.filter_by(id=pid).first()
        if not post:
            return generate_res('failed', 'post not found')
        post.set_attrs(data)

        # TODO:优化 每次修改tag,都要删除之前的tag
        post.tags.clear()
        [post.tags.append(Tag.query.filter_by(name=new_tag).first() or Tag(new_tag)) for new_tag in tags]
        post.auto_commit()
        return generate_res('success', 'add posts')
    pid = data.get('id')
    post = Post.query.filter_by(id=pid).first()
    data = {"id": post.id, "contents": post.contents, "title": post.title, "tags": [tag.name for tag in post.tags]}
    return generate_res('success', 'get post', data=data)


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


@api.route('/admin/auth/logout/', methods=["DELETE"])
@required_login
def admin_logout():
    uid = request.headers.get('identify')
    user = User.query.filter_by(id=uid).first()
    user.is_active = False
    user.auto_commit()
    return generate_res('success', 'logout')
