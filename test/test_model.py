from app.model.db import User, Post, Tag, db
from collections import namedtuple
from app.utils import get_now_timestamp
from app.exception import NotFound
import pytest

uid = ''


class TestUser:
    def test_set_password(self):
        with db.auto_commit():
            user = User(email='101242@gmail.com', email_is_validate=True)
            user.set_password('password')
            db.session.add(user)
        user.check_password('password')
        global uid
        uid = user.id

    def test_set_code(self):
        Email = namedtuple('Email', 'data')
        Code = namedtuple('code', 'data')
        Form = namedtuple('Form', 'email code')
        code, _ = User.set_code_by(uid=uid)
        form = Form(
            email=Email('101242@gmail.com'),
            code=Code(code)
        )
        user = User.validate_code(form)
        assert user is not None


class TestPost:
    def test_set_links(self):
        with db.auto_commit():
            post = Post()
            post._set_links('/test/url/com')
            db.session.add(post)
        assert post.links is not None

    def test_set_tags(self):
        with db.auto_commit():
            post = Post(title='test', change_date=get_now_timestamp())
            post._set_tags(['tag', 'tags', 'tag1'])
            db.session.add(post)
        assert post.comments == 0
        assert len(post.tags) == 3

    def test_create(self):
        post = Post.create(
            title='test',
            change_date=get_now_timestamp(),
            tags=['tag', 'tags', 'tag1'],
            links='/test/url/com'
        )
        assert len(post.tags) == 3
        assert len(post.links) == 1

    @pytest.mark.xfail(NotFound)
    def test_search_delete(self):
        pagination = Post.paging_search(
            page=1,
            per_page=2,
            order_by=db.desc('id')
        )
        items = pagination.items
        assert len(items) != 0
        post = items[0]
        Post.delete_by_id(post.id)
        Post().search_by(id=post.id)


class TestTag:
    def test_query_post(self):
        tags = Tag.query.all()
        tag = tags[0]
        assert len(tag.posts) != 0
