import time
from io import BytesIO

import pytest
from faker import Faker
from flask import url_for

faker = Faker('zh_CN')
pid = 0
token = ''
uid = ''
username = faker.name()
nickname = faker.name()
email = faker.email()
phone = faker.phone_number()
password = faker.password()
timeStamp = int(time.time() * 1000)


class Test_auth:
    def test_register(self, client):
        res = client.post(url_for('api.admin_register'), json={
            'username': username,
            'nickname': nickname,
            'email': email,
            'phone': phone,
            'password': password
        })
        assert b'success' in res.data

    def test_login(self, client):
        res = client.post(url_for('api.admin_login'), json={
            'username': username,
            'password': password
        })
        global token, uid
        data = res.get_json()
        token = data.get('token')
        uid = data.get('id')
        assert b'success' in res.data


# --repeat-scope=class
@pytest.mark.repeat(4)
class Test_posts:
    def test_admin_posts_post(self, client):
        print(1)
        res = client.post(url_for('api.admin_posts'), headers={
            'identify': uid,
            'Authorization': token
        })

        global pid
        pid = res.get_json().get('id')
        assert b'success' in res.data
        assert res.status_code == 200

    def test_admin_posts_put(self, client):
        print(2)
        res = client.put(url_for('api.admin_posts'), json={
            'id': pid,
            'title': 'title'
            ,
            'timeStamp': timeStamp,
            'contents': 'contests',
            'tags': ['tags2', 'tags1', 'tags3'],
            'publish': True,
        }, headers={
            'identify': uid,
            'Authorization': token
        })
        assert b'success' in res.data

    def test_admin_posts_get(self, client):
        res = client.get(url_for('api.admin_posts'), headers={
            'identify': uid,
            'Authorization': token
        })
        assert b'success' in res.data


class Test_image:
    def test_admin_image_post(self, client):
        with open('/home/pjs/Pictures/epoll.png', 'rb') as f:
            pic = f.read()
        data = {'images': (BytesIO(pic), 'images.png'), 'id': pid}
        res = client.post(
            url_for('api.admin_images'),
            content_type='multipart/form-data',
            data=data,
            headers={
                'identify': uid,
                'Authorization': token
            })
        assert b'success' in res.data

    def test_admin_image_get(self, client):
        data = {
            "id": pid,
            "filename": 'images.png'
        }
        res = client.get(url_for('api.admin_images'), json=data, headers={
            'identify': uid,
            'Authorization': token
        })
        assert res.status_code == 200
