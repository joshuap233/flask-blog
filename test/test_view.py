from flask import url_for


def test_archive(client):
    res = client.get(url_for('api.archive', page=1))
    assert b'success' in res.data


def test_post(client):
    res = client.get(url_for("api.posts", post_id=1))
    assert b'success' in res.data


def test_tags(client):
    res = client.get(url_for('api.tags'))
    assert b'success' in res.data
