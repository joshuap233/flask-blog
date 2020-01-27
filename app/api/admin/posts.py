import time

from flask import request

from .blueprint import admin
from app.database import Post
from app.utils import generate_res, required_login


@admin.route("/posts/")
@required_login
def posts_view():
    order_by = request.args.get('orderBy')
    if order_by:
        pass
    search = request.args.get('search')
    if search:
        # TODO: 搜索(标签,日期,标题,时间),排序
        data = {
            'total': 20,  # 所有文章数
            'page': 1,  # 页数,从第0页开始
            'post': [{
                'postId': 1,
                'title': 'title1',
                'tags': 'tags2,tag3',
                'visibility': '私密',
                'comments': 2,
                'changeDate': '2018/2/10 12:10',
                'createDate': '2018/2/10 12:10'
            }]}
        return generate_res('success', 'msg', data=data)
    page = int(request.args.get('page'))
    page_size = int(request.args.get('pageSize'))
    pagination = Post.query.paginate(page=page, page_size=page_size, error_out=False)
    posts = pagination.items
    if not posts:
        return generate_res('failed', 'page not found'), 404
    data = [{'postId': post.id,
             'title': post.title,
             'tags': ",".join([tag['name'] for tag in post.tags]),
             'visibility': post.visibility,
             'createDate': time.strftime("%Y/%m/%d %H:%M", time.localtime(post.createDate)),
             'changeDate': time.strftime("%Y/%m/%d %H:%M", time.localtime(post.changeDate))}
            for post in posts]
    return generate_res('success', 'msg', data={
        'total': Post.total(),
        'page': page,
        'post': data
    })
