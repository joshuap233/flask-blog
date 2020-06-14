import pytest
from flask import url_for
import json
from app.signals import email_signals, login_signal_sender

POST = {
    'id': -1,
    'title': 'title',
    'article': 'contests',
    'tags': ['tags1', 'tags2', 'tags3'],
    'visibility': '私密',
    'create_date': '2019/2/10 10:20',
    'change_date': '2019/10/2 2:10',
    'excerpt': '摘抄'
}

user_info = {
    'username': 'username',
    'nickname': 'nickname',
    'password': 'password123',
    'confirm_password': 'password123'
}

headers = {
    'identify': '',
    'Authorization': ''
}

"""
解析查询参数
'orderBy':'[{field:'title',desc:True/False}]
'page':'0',
'pageSize':'10',
'search':'str',
'totalCount':'1',
'filter_by':{tid:1}
"""

POST_QUERY = {
    'page': 0,
    'pageSize': 10,
    'search': 'title',
    'orderBy': json.dumps([{"field": "title", "desc": True}])
}


def test_login(client):
    res = client.post(
        url_for('admin.register_view'),
        json=user_info
    )

    assert b'success' in res.data
    res = client.post(
        url_for('admin.login_view'),
        json=user_info
    )
    data = res.get_json().get('data')
    headers['identify'] = data.get('id')
    headers['Authorization'] = f'Bearer {data.get("token")}'


# --repeat-scope=class
# @pytest.mark.repeat(4)
class Test_post_view:
    @pytest.mark.repeat(4)
    def test_post_post(self, client):
        res = client.post(url_for('admin.post_view'), headers=headers)
        POST['id'] = res.get_json().get('data').get('id')
        assert b'success' in res.data

    @pytest.mark.repeat(4)
    def test_post_put(self, client):
        res = client.put(url_for('admin.post_view', pid=POST['id']), json=POST, headers=headers)
        assert b'success' in res.data

    def test_post_get(self, client):
        res = client.get(url_for('admin.post_view', pid=POST['id']), headers=headers)
        data = res.get_json().get('data')
        assert 'title' in data and 'tags' in data

    def test_post_delete(self, client):
        res = client.delete(url_for('admin.post_view'), headers=headers, json={
            'id_list': [POST['id']]
        })
        assert b'success' in res.data

        # 测试是否删除成功
        res = client.delete(url_for('admin.post_view'), headers=headers, json={
            'id_list': [POST['id']]
        })
        assert b'failed' in res.data


class Test_posts_view:
    # 测试搜索功能
    def test_get_query(self, client):
        res = client.get(url_for('admin.posts_view', **POST_QUERY), headers=headers)
        assert b'success' in res.data
