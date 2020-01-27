# TODO: 抽离数据处理, 表单验证
import os

from flask import request, current_app, send_from_directory, url_for

from .blueprint import api
from ..database import Post, Tag, User
from ..utils import required_login, generate_res, get_attr, send_email


@api.route('/admin/images/', methods=['GET', 'PUT'])
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
    return send_from_directory(os.path.join(current_app.config['UPLOAD_FOLDER'], str(pid)), filename)


# 分页查询
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


# put修改文章, post新增文章, get获取单篇文章内容
@api.route('/admin/posts/', methods=['POST', 'DELETE'], defaults={"pid": ''})
@api.route('/admin/posts/<int:pid>', methods=['GET', 'PUT'])
@required_login
def admin_post(pid):
    data = request.get_json()
    if request.method == 'POST':
        # 添加新文章
        try:
            create_date = data.get('create_date')
        except AttributeError:
            return generate_res("failed", "empty create_date")
        post = Post(create_date=create_date)
        post.auto_add()
        return generate_res('success', 'new post', id=post.id)
    elif request.method == 'PUT':
        try:
            # 前端生成空标签列表
            tags = data.get('tags')
        except AttributeError:
            return generate_res('failed', 'get post id and tags failed')
        post = Post.query.filter_by(id=pid).first()
        if not post:
            return generate_res('failed', 'post not found')
        post.set_attrs(data)

        # TODO:优化 每次修改tag,都要删除之前的tag
        post.tags.clear()
        [post.tags.append(Tag.query.filter_by(name=new_tag).first() or Tag(new_tag)) for new_tag in tags]
        post.auto_add()
        return generate_res('success', 'add posts')
    elif request.method == 'DELETE':
        pids: list = data.get('delete_posts')
        posts = []
        for pid in pids:
            post = Post.query.filter_by(id=pid).first()
            if post is None:
                posts.append(pid)
                continue
            post.auto_delete()
        return generate_res('success', 'delete', data=posts)
    post = Post.query.filter_by(id=pid).first()
    data = {"id": post.id, "contents": post.contents, "title": post.title, "tags": [tag.name for tag in post.tags]}
    return generate_res('success', 'get post', data=data)