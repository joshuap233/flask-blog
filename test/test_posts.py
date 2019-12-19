from flask import url_for


def test_post(client):
    res = client.get(url_for("api.posts", post_id=1))
    assert b'success' in res.data
