import os

from faker import Faker
from flask import url_for

from app.model.db import User

faker = Faker('zh_CN')
pid = 0
token = ''
uid = ''
username = faker.name()
nickname = faker.name()
email = os.getenv('MAIL_RECEVIER')
phone = faker.phone_number()
password = faker.password()
print('test111', os.getenv('MAIL_RECEVIER'))


class Test_auth:
    def test_register(self, client):
        res = client.post(url_for('admin.admin_register'), json={
            'username': username,
            'nickname': nickname,
            'email': email,
            'phone': phone,
            'password': password
        })
        assert b'success' in res.data

    def test_admin_auth_register(self, client):
        user = User.query.filter_by(email=email).first()
        user.auto_delete()
        user = User()
        user.set_attrs({
            'username': username,
            'nickname': nickname,
            'email': email,
            'phone': phone,
            'password': password
        })
        user.auto_add()
        res = client.get(url_for('admin.admin_auth_register', token=user.generate_token()))
        assert b'success' in res.data

    def test_login(self, client):
        res = client.post(url_for('admin.admin_login'), json={
            'username': username,
            'password': password
        })
        global token, uid
        data = res.get_json()
        token = data.get('token')
        uid = data.get('id')
        assert b'success' in res.data


# --repeat-scope=class
# @pytest.mark.repeat(4)
# class Test_posts:
#     def test_admin_post_post(self, client):
#         res = client.post(url_for('admin.admin_post'), json={
#             'create_date': timeStamp,
#         }, headers={
#             'identify': uid,
#             'Authorization': token
#         })
#
#         global pid
#         pid = res.get_json().get('id')
#         assert b'success' in res.data
#         assert res.status_code == 200
#
#     def test_admin_post_put(self, client):
#         res = client.put(url_for('admin.admin_post', pid=pid), json={
#             'title': 'title'
#             ,
#             'change_date': timeStamp,
#             'contents': 'contests',
#             'tags': ['tags1', 'tags2', 'tags3'],
#             'publish': True,
#         }, headers={
#             'identify': uid,
#             'Authorization': token
#         })
#         assert b'success' in res.data
#
#     def test_admin_post_get(self, client):
#         res = client.get(url_for('admin.admin_post', pid=pid), headers={
#             'identify': uid,
#             'Authorization': token
#         }, json={
#             "id": 1
#         })
#         data = res.get_json().get('data')
#         assert 'title' in data and 'contents' in data and 'tags' in data
#
#     def test_admin_posts_page(self, client):
#         res = client.get(url_for('admin.admin_posts', page=1), headers={
#             'identify': uid,
#             'Authorization': token
#         })
#         data = res.get_json().get('data')
#         assert b'success' in res.data
#         for d in data:
#             assert 'title' in d and 'create_date' in d and 'publish' in d
#
#
# class test_admin_delete:
#
#     def test_admin_post_delete(self, client):
#         res = client.delete(url_for('admin.admin_post'), json={
#             "delete_posts": [1]
#         }, headers={
#             'identify': uid,
#             'Authorization': token
#         })
#         data = res.get_json().get('data')
#         assert len(data) == 0
#
#     def test_admin_post_auth_delete(self, client):
#         res = client.delete(url_for('admin.admin_post'), json={
#             "delete_posts": [1]
#         }, headers={
#             'identify': uid,
#             'Authorization': token
#         })
#         data = res.get_json().get('data')
#         assert len(data) != 0
#

class Test_logout:
    def test_logout(self, client):
        print(token)
        res = client.delete(url_for('admin.admin_logout'), headers={
            'identify': uid,
            'Authorization': token
        })
        assert b'success' in res.data

    # 测试是否注销成功
    def test_admin_posts(self, client):
        res = client.get(url_for('admin.post_view'), headers={
            'identify': uid,
            'Authorization': token
        })
        assert res.status_code == 401
        assert b'failed' in res.data
