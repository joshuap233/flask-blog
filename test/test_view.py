from flask import url_for


def test_archive(client):
    res = client.get(url_for('api.archive', page=1))
    data = res.get_json().get('data')
    for d in data:
        assert d.get('date') is not None
        for article in d['articles']:
            assert len(article) is not 0
    assert b'success' in res.data


def test_post(client):
    res = client.get(url_for("api.posts", post_id=1))
    data:dict = res.get_json().get('data')
    assert b'success' in res.data
    # assert data


def test_tags(client):
    res = client.get(url_for('api.tags'))
    assert b'success' in res.data
