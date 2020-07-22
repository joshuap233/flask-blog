from flask import url_for

from app.model.db import Post, Tag, Comment
from app.model.view import BaseQueryView
from app.model.view import BaseView, TableView


class IdView(BaseView):
    def __init__(self, source):
        self.id = source.id


class PostView(BaseView):
    def __init__(self, post, excerpt=False, article=True):
        self.id = post.id
        self.title = post.title or ''
        self.tags = [{'id': tag.id, 'name': tag.name} for tag in post.tags]
        self.time = post.change_date
        self.commentsCount = post.comments  # 评论数量
        if article:
            self.content = post.article_html
        if excerpt:
            self.excerpt = post.excerpt
            self.illustration = ImageUrlView(post.illustration.url).url if post.illustration else None


class PostsView(BaseView, TableView):
    def __init__(self, posts, page):
        super(PostsView, self).__init__(posts, page, Post)

    @staticmethod
    def _fill(posts):
        return [PostView(post, excerpt=True, article=False) for post in posts]


class ImageUrlView(BaseView):
    def __init__(self, filename):
        self.name = filename
        self.url = url_for('api.send_images_view', filename=filename, _external=True)


class TagView(BaseView):
    def __init__(self, tag):
        self.id = tag.id
        self.name = tag.name
        # self.count = tag.count
        self.describe = tag.describe
        self.image = ImageUrlView(tag.link.url) if tag.link else ''


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
        self.articleCount = Post.total()
        self.tagsCount = Tag.total()


class ArchiveView(BaseView, TableView):
    def __init__(self, posts, page):
        super(ArchiveView, self).__init__(posts, page, Post)

    @staticmethod
    def _fill(posts):
        return [PostView(post, excerpt=False, article=False) for post in posts]


class CommentView(BaseView):
    def __init__(self, comment: Comment):
        self.id = comment.id
        self.post_id = comment.post_id
        self.content = comment.content
        self.nickname = comment.nickname
        self.browser = comment.browser
        self.system = comment.system
        self.website = comment.website
        self.email = comment.email
        self.create_date = comment.create_date
        self.parent_id = comment.parent_id


class CommentsView(BaseView, TableView):
    def __init__(self, comment, page):
        super().__init__(comment, page, Comment)

    @staticmethod
    def _fill(comments):
        return [CommentView(comment) for comment in comments] if comments else []


class PostsQueryView(BaseQueryView):
    @staticmethod
    def _get_order_by() -> list:
        return [{'field': 'id'}]


class TagsQueryView(BaseQueryView):
    @staticmethod
    def _get_order_by() -> list:
        return [{'field': 'id'}]
