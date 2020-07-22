from app.model.view import BaseView, TableView, BaseComment
from flask import url_for, current_app
from app.model.db import Post, Tag, Comment, CommentReply
from app.model.view import BaseQueryView


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


class ReplyView(BaseComment):
    def __init__(self, reply: CommentReply):
        super(ReplyView, self).__init__(reply, show=False, email=False, ip=False)
        self.comment_id = reply.comment_id
        self.parent_id = reply.parent_id


class RepliesView(BaseView, TableView):
    def __init__(self, replies, page):
        super().__init__(replies, page, CommentReply)

    @staticmethod
    def _fill(replies):
        return [ReplyView(reply) for reply in replies] if replies else []


class CommentView(BaseComment):
    def __init__(self, comment: Comment):
        super(CommentView, self).__init__(comment, show=False, email=False, ip=False)
        # self.post_id = comment.post_id
        # self.post_title = comment.posts.title
        self.reply = RepliesView(self._get_replies(comment), 0)

    @staticmethod
    def _get_replies(comment):
        # 获取前SUB_COMMENT_PAGE_SIZE个子评论
        return comment.comment_reply.order_by(CommentReply.create_date.desc()).limit(
            current_app.config['PAGESIZE']
        ).all()


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
