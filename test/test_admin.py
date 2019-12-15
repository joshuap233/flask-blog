import time
from io import BytesIO

from flask import url_for

time = int(time.time())
token = ''
uid = ''


def test_register(client):
    res = client.post(url_for('api.admin_register'), json={
        'username': 'username',
        'nickname': 'nickname',
        'email': 'email@gmail.com',
        'phone': '12323172013',
        'password': 'password'
    })
    assert b'success' in res.data


def test_login(client):
    res = client.post(url_for('api.admin_login'), json={
        'username': 'username',
        'password': 'password'
    })
    global token, uid
    data = res.get_json()
    token = data.get('token')
    uid = data.get('id')
    assert b'success' in res.data


def test_admin_posts_post(client):
    res = client.post(url_for('api.admin_posts'), json={
        'timeStamp': time
    }, headers={
        'identify': uid,
        'Authorization': token
    })

    # data = res.get_json()
    # assert data['status'] == 'success'
    assert b'success' in res.data
    assert res.status_code == 200


def test_admin_posts_put(client):
    res = client.put(url_for('api.admin_posts'), json={
        'title': 'title1',
        'timeStamp': time,
        'content': 'contests',
        'tags': ['tags2', 'tags1', 'tags3'],
        'publish': True,
    }, headers={
        'identify': uid,
        'Authorization': token
    })
    assert b'success' in res.data


def test_admin_posts_get(client):
    res = client.get(url_for('api.admin_posts'), headers={
        'identify': uid,
        'Authorization': token
    })
    assert b'success' in res.data


def test_admin_image_post(client):
    with open('/home/pjs/Pictures/epoll.png', 'rb') as f:
        pic = f.read()
    data = {'images': (BytesIO(pic), 'images.png'), 'timeStamp': time}
    res = client.post(
        url_for('api.admin_images'),
        content_type='multipart/form-data',
        data=data, headers={
            'identify': uid,
            'Authorization': token
        })
    assert b'success' in res.data


def test_admin_get(client):
    res = client.get(url_for('api.admin_images', timeStamp=time, filename='images.png'), headers={
        'identify': uid,
        'Authorization': token
    })
    assert res.status_code == 200
