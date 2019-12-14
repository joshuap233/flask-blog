import time
from io import BytesIO

from flask import url_for

time = int(time.time())


def test_admin_posts_post(client):
    res = client.post(url_for('api.admin_posts'), json=dict({
        'timeStamp': time
    }))

    # data = res.get_json()
    # assert data['status'] == 'success'
    assert b'success' in res.data
    assert res.status_code == 200


def test_admin_posts_put(client):
    res = client.put(url_for('api.admin_posts'), json=dict({
        'title': 'title1',
        'timeStamp': time,
        'content': 'contests',
        'tags': ['tags2', 'tags1', 'tags3'],
        'publish': True,
    }))
    assert b'success' in res.data


def test_admin_posts_get(client):
    res = client.get(url_for('api.admin_posts'), )
    assert b'success' in res.data


def test_admin_image_post(client):
    with open('/home/pjs/Pictures/epoll.png', 'rb') as f:
        pic = f.read()
    data = {'images': (BytesIO(pic), 'images.png'), 'timeStamp': time}
    res = client.post(
        url_for('api.admin_images'),
        content_type='multipart/form-data',
        data=data)
    assert b'success' in res.data


def test_admin_get(client):
    res = client.get(url_for('api.admin_images', timeStamp=time, filename='images.png'))
    assert res.status_code == 200


def test_user(client):
    pass
