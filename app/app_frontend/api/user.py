from app.model.db import User, Post, Tag
from app.utils import generate_res
from .blueprint import api


# TODO
@api.route('/user/info')
def about():
    user = User.query.first()
    return generate_res(data={
        "about": user.about_html,
        "avatar": user.avatar,
        "nickname": user.nickname,
        "ICP": '',
        'motto': '',
        'articleCount': Post.total(visibility=True),
        'tagsCount': Tag.total(visibility=True),
        # 放入配置
        # "github": user.github,
        # "twitter": user.twitter,
        # "email": user.email,
    })
