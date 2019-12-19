from flask import url_for


def test_archive(client):
    res = client.get(url_for('api.archive', page=1))
    assert b'success' in res.data
