from flask import url_for

from app.model.db import Tag, Post, Link, Comment, CommentReply
from app.model.view import BaseView, TableView, BaseComment
from app.utils import format_time


class IdView(BaseView):
    def __init__(self, source):
        self.id = source.id


class PostView(BaseView):
    def __init__(self, post, article=True, excerpt=True):
        self.id = post.id
        self.title = post.title or ''
        self.tags = [tag.name for tag in post.tags]
        self.visibility = post.visibility
        self.create_date = format_time(post.create_date)
        self.change_date = format_time(post.change_date)
        self.comments = post.comments
        if article:
            self.article = post.article or ''
        if excerpt:
            self.excerpt = post.excerpt
            self.illustration = ImageUrlView(post.illustration.url).url if post.illustration else ''
            self.excerpt_rich_text = post.excerpt_rich_text
            self.isRichText = post.isRichText


# 格式化从数据库获取的文章
class PostsView(BaseView, TableView):
    def __init__(self, posts: dict, page: int):
        super().__init__(posts, page, Post)

    @staticmethod
    def _fill(posts):
        return [PostView(post, article=False, excerpt=False) for post in posts]


# 格式化从数据库获取的标签
class TagsView(BaseView, TableView):
    def __init__(self, tags, page):
        super().__init__(tags, page, Tag)

    @staticmethod
    def _fill(tags):
        return [TagView(tag) for tag in tags] if tags else []


class TagView(BaseView):
    def __init__(self, tag):
        self.id = tag.id
        self.name = tag.name or ''
        self.describe = tag.describe
        self.count = tag.count
        self.image = ImageUrlView(tag.link.url if tag.link else '')


class UserInfoView(BaseView):
    def __init__(self, user):
        self.nickname = user.nickname
        self.username = user.username
        self.email = user.email
        self.about = user.about
        self.about_html = user.about_html
        self.avatar = user.avatar
        self.icp = user.icp
        self.motto = user.motto
        self.set_field_not_None()
        self.password = ''


class LoginView(BaseView):
    def __init__(self, user):
        self.id = user.id
        self.token = user.generate_login_token()


# 多张图片
class ImagesView(BaseView, TableView):
    def __init__(self, links, page):
        super().__init__(links, page, Link)

    @staticmethod
    def _fill(links):
        return [ImageView(link) for link in links] if links else []


class NewImagesView(BaseView):
    def __init__(self, links):
        self.values = [NewImageView(link) for link in links]


# 添加新图片时,发送图片id, 与链接
class NewImageView(BaseView):
    def __init__(self, link):
        self.id = link.id
        self.image = ImageUrlView(link.url)


# 图片详细信息
class ImageView(BaseView):
    def __init__(self, link):
        self.id = link.id
        self.image = ImageUrlView(link.url)
        self.describe = link.describe
        # 图片被使用次数
        self.relationship = self._get_relationship(link)
        self.count = self._get_count()

    def _get_count(self):
        return len(self.relationship)

    @staticmethod
    def _get_relationship(link):
        relationship = [{'id': post.id, 'name': post.title, 'type': '文章'} for post in link.posts]
        relationship.extend([
            {'id': tag.id, 'name': tag.name, 'type': '标签'} for tag in link.tags
        ])
        return relationship


# 获取所有标签名
class AllTagsView(BaseView):
    def __init__(self):
        self.data = [
            tag.name for tag in Tag.query.all()
        ]


# 图片url
class ImageUrlView(BaseView):
    def __init__(self, filename):
        self.name = filename
        self.url = url_for('admin.send_images_view', filename=filename, _external=True) if filename else ''


class ReplyView(BaseComment):
    def __init__(self, reply: CommentReply):
        super(ReplyView, self).__init__(reply)
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
        super(CommentView, self).__init__(comment)
        self.post_id = comment.post_id
        self.post_title = comment.posts.title
        # self.subRows = RepliesView(self._get_replies(comment), 0).values

    @staticmethod
    def _get_replies(comment):
        # 获取前SUB_COMMENT_PAGE_SIZE个子评论
        # return comment.comment_reply.order_by(CommentReply.create_date.desc()).limit(
        #     current_app.config['SUB_COMMENT_PAGE_SIZE']).all()
        return comment.comment_reply.all()


class CommentsView(BaseView, TableView):
    def __init__(self, comment, page):
        super().__init__(comment, page, Comment)

    @staticmethod
    def _fill(comments):
        return [CommentView(comment) for comment in comments] if comments else []
