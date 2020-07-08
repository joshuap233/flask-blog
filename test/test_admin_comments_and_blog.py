from faker import Faker
from flask import url_for

faker = Faker('zh_CN')

headers = {
    'identify': '',
    'Authorization': ''
}

user_info = {
    'username': 'username',
    'nickname': 'nickname',
    'password': 'password123',
    'confirm_password': 'password123'
}
TAGS = []


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
