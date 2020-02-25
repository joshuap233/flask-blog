import os
import random

import pytest
from faker import Faker
from flask import url_for

from app.model.db import User

faker = Faker('zh_CN')

HEADERS = {
    'identify': '',
    'Authorization': ''
}

POST_QUERY = {
    'filters': '[1, 2, 3]',
    'page': 0,
    'pageSize': 10,
    'search': 'title',
    'orderBy': '{"field": "title", "title": "test"}',
    'orderDirection': random.choice(["asc", "desc"]),
}

TAG_QUERY = {
    'page': 0,
    'pageSize': 10,
}

USER = {
    'username': faker.name(),
    'nickname': faker.name(),
    'email': os.getenv('MAIL_RECEVIER', 'exmaple.@gmail.com'),
    'password': 'password123',
    'confirm_password': 'password123'
}

POST = {
    'id': -1,
    'title': 'title',
    'article': 'contests',
    'tags': ['tags1', 'tags2', 'tags3'],
    'visibility': '私密',
    'create_date': '2019/2/10 10:20',
    'change_date': '2019/10/2 2:10',
    'excerpt': '摘抄'
}
TAG = {
    'id': 1,
    'name': 'tags1',
    'describe': 'describe',
}

TAGS = []


class Test_auth:
    def test_register(self, client):
        res = client.post(url_for('admin.register_view'), json=USER)
        data = res.get_json().get('data')
        uid = data.get('id')
        assert uid is not None
        global HEADERS
        HEADERS['identify'] = uid
        assert b'success' in res.data

    # 添加邮件,并认证
    def test_auth_register(self, client):
        user = User.query.get(HEADERS['identify'])
        res = client.get(url_for('admin.auth_email_view', token=user.generate_token()))
        assert b'success' in res.data

    # 测试用户名登录
    def test_login(self, client):
        res = client.post(url_for('admin.login_view'), json=USER)
        global HEADERS
        data = res.get_json().get('data')
        HEADERS['Authorization'] = data.get('token')
        HEADERS['identify'] = data.get('id')
        assert b'success' in res.data


# --repeat-scope=class
# @pytest.mark.repeat(4)
class Test_post_view:
    @pytest.mark.repeat(4)
    def test_post_post(self, client):
        res = client.post(url_for('admin.post_view'), headers=HEADERS)

        global POST
        POST['id'] = res.get_json().get('data').get('id')
        assert b'success' in res.data
        assert res.status_code == 200

    @pytest.mark.repeat(4)
    def test_post_put(self, client):
        res = client.put(url_for('admin.post_view'), json=POST, headers=HEADERS)
        assert b'success' in res.data

    def test_post_get(self, client):
        res = client.get(url_for('admin.post_view', id=POST['id']), headers=HEADERS)
        data = res.get_json().get('data')
        assert 'title' in data and 'tags' in data

    def test_post_delete(self, client):
        res = client.delete(url_for('admin.post_view'), json={
            'id': POST['id']
        }, headers=HEADERS)
        assert b'success' in res.data

    # 测试是否删除成功
    def test_auth_post_delete(self, client):
        res = client.delete(url_for('admin.post_view'), json={
            "id": POST['id']
        }, headers=HEADERS)
        assert b'failed' in res.data


class Test_posts_view:
    # 测试搜索功能
    def test_get_query(self, client):
        res = client.get(url_for('admin.posts_view', **POST_QUERY), headers=HEADERS)
        assert b'success' in res.data


class Test_tags_view:

    # 测试带参查询
    def test_tags_get(self, client):
        res = client.get(url_for('admin.tags_view'), headers=HEADERS)
        assert b'success' in res.data
        global TAGS
        global TAG
        TAGS.extend(res.get_json()['data']['tags'])
        TAG = TAGS[0]
        assert len(TAGS) != 0

    def test_get_all_tags(self, client):
        # 该接口用于前端标签名自动提示
        res = client.get(url_for('admin.all_tags_view'), headers=HEADERS)
        assert b'success' in res.data

    # 添加标签
    def test_tags_post(self, client):
        res = client.post(url_for('admin.tags_view'), headers=HEADERS)
        id_ = res.get_json()['data']['id']
        assert b'success' in res.data
        res = client.put(url_for('admin.tags_view'), headers=HEADERS, json={
            'id': id_,
            'name': str(random.randint(0, 1000)),
            'describe': 'describe123'
        })
        assert b'success' in res.data

    # 修改标签名
    def test_tags_put(self, client):
        tag = TAGS[0]
        tag['name'] = 'tags222' + str(random.randint(1, 10000))
        res = client.put(url_for('admin.tags_view'), headers=HEADERS, json=tag)
        assert b'success' in res.data

        # 测试标签名重复的情况
        tag['name'] = 'tags2'
        res = client.put(url_for('admin.tags_view'), headers=HEADERS, json=tag)
        assert b'failed' in res.data

    def test_upload_tag_img(self, client):
        # f = open(os.getenv('TEST_PIC_PATH'), "rb")
        import io
        data = {
            'id': TAG['id'],
            'image': (io.BytesIO(b"my tag images"), 'tag1.jpg')
        }
        res = client.post(
            url_for('admin.tags_pic_view'),
            data=data,
            content_type='multipart/form-data',
            headers=HEADERS
        )
        assert b'success' in res.data

    def test_img_get(self, client):
        pass
        # res = client.get(
        #     url_for('admin.tags_pic_view', **{'tag_name': 'test'}),
        #     headers=HEADERS
        # )

    def test_tags_delete(self, client):
        res = client.delete(url_for('admin.tags_view'), headers=HEADERS, json=TAGS[0])
        assert b'success' in res.data

        # 确认是否删除成功
        res = client.delete(url_for('admin.tags_view'), headers=HEADERS, json=TAGS[0])
        assert b'failed' in res.data


class Test_logout:
    def test_logout(self, client):
        res = client.delete(url_for('admin.logout_view'), headers=HEADERS)
        assert b'success' in res.data

        # 测试是否注销成功
        res = client.get(url_for('admin.post_view'), headers=HEADERS)
        assert res.status_code == 401
        assert b'failed' in res.data
