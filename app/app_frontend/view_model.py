from app.model.view import BaseView
from flask import url_for
from app.model.db import Post, Tag


class PostView(BaseView):
    def __init__(self, post):
        self.id = post.id
        self.title = post.title or ''
        self.tags = [{'id': tag.id, 'name': tag.name} for tag in post.tags]
        self.change_date = post.change_date
        self.article = post.article_html
        self.comments = post.comments


class PostsView(BaseView):
    def __init__(self, posts, page):
        self.content = self._fill(posts)
        self.page = page

    @staticmethod
    def _fill(posts):
        content = []
        for item in posts:
            post = PostView(item)
            del post.article
            content.append(post)
        return content


class ImageUrlView(BaseView):
    def __init__(self, filename):
        self.name = filename
        self.url = url_for('api.send_images_view', filename=filename, _external=True)


class TagView(BaseView):
    def __init__(self, tag):
        self.id = tag.id
        self.name = tag.name
        self.count = tag.count
        self.describe = tag.describe
        self.image = ImageUrlView(tag.link.url if tag.link else '')


class TagsView(BaseView):
    def __init__(self, tags):
        self.content = self._fill(tags)

    @staticmethod
    def _fill(tags):
        return [TagView(tag) for tag in tags]


class UserInfoView(BaseView):
    def __init__(self, user):
        self.about = user.about_html
        self.avatar = user.avatar
        self.nickname = user.nickname
        self.icp = user.icp
        self.motto = user.motto
        self.articleCount = Post.total(visibility=True)
        self.tagsCount = Tag.total(visibility=True)
        # 放入配置
        # github: user.github
        # twitter: user.twitter
        # email: user.email
