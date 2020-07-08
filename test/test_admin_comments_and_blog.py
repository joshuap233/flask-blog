from flask import url_for
from .data import headers, user_info


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
