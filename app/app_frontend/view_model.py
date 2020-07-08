from app.model.view import BaseView, TableView
from flask import url_for
from app.model.db import Post, Tag


class PostView(BaseView):
    def __init__(self, post, excerpt=False, article=True):
        self.id = post.id
        self.title = post.title or ''
        self.tags = [{'id': tag.id, 'name': tag.name} for tag in post.tags]
        self.change_date = post.change_date
        self.comments = post.comments  # 评论数量
        if article:
            self.article = post.article_html
        if excerpt:
            self.excerpt = post.excerpt_html


class PostsView(BaseView, TableView):
    def __init__(self, posts, page):
        super(PostsView, self).__init__(posts, page, Post)

    @staticmethod
    def _fill(posts):
        return [PostView(post, excerpt=True, article=True) for post in posts]


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
        self.values = self._fill(tags)

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


class ArchiveView(BaseView, TableView):
    def __init__(self, posts, page):
        super(ArchiveView, self).__init__(posts, page, Post)

    @staticmethod
    def _fill(posts):
        return [PostView(post) for post in posts]
