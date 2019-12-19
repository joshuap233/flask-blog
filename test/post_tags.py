from flask import url_for


def test_tags(client):
    res = client.get(url_for('api.tags'))
    assert b'success' in res.data
