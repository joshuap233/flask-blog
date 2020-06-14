# from flask import url_for
#
#
# def test_post(client):
#     res = client.get(url_for("api.posts", post_id=1))
#     data = res.get_json().get('data')
#     assert b'success' in res.data
#     assert 'id' in data
#     assert 'title' in data
#     assert 'contents' in data
#
#
# def test_tags(client):
#     res = client.get(url_for('api.tags'))
#     data = res.get_json().get('data')
#     assert b'success' in res.data
#     for d in data:
#         assert 'name' in d
#         assert 'article' in d
#         assert len(d['article']) != 0
#
#
# def test_about(client):
#     res = client.get(url_for('api.about'))
#     assert b'success' in res.data
