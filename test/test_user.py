from flask import url_for
import pytest
from app.model.db import User

user = {
    'username': 'username',
    'email': '123123@gmail.com',
    'password': 'password',
    'confirm_password': 'password'
}

user_info = {
    'username': 'username',
    'nickname': 'nickname',
    'avatar': 'avatar',
    'about': 'about'
}
headers = {
    'identify': '',
    'Authorization': ''
}


class TestUser(object):

    def test_register(self, client):
        res = client.post(
            url_for('admin.register_view'),
            json=user
        )
        assert b'success' in res.data

    def test_login(self, client):
        res = client.post(
            url_for('admin.login_view'),
            json={
                'username': 'username',
                'password': 'password'
            }
        )
        assert b'success' in res.data
        data = res.get_json().get('data')
        id_ = data.get('id')
        token = data.get('token')
        assert id_ is not None
        assert token is not None
        global headers
        headers['identify'] = id_
        headers['Authorization'] = f'Bearer {token}'

    def test_email_auth(self, client):
        user_ = User.query.get_or_404(headers['identify'])
        token = user_.generate_access_token()
        res = client.get(url_for('admin.auth_email_view', token=token))
        assert b'success' in res.data

    def test_fake_email_token(self, client):
        res = client.get(url_for('admin.auth_email_view', token='test'))
        assert b'failed' in res.data

    def test_auth(self, client):
        res = client.get(url_for('admin.auth_view'), headers=headers)
        assert b'success' in res.data

    def test_user_info_without_auth_header(self, client):
        res = client.get(url_for('admin.user_info_view'))
        assert b'success' not in res.data

    def test_get_user_info(self, client):
        res = client.get(url_for('admin.user_info_view'), headers=headers)
        assert b'success' in res.data
        data = res.get_json().get('data')
        username = data.get('username')
        avatar = data.get('avatar')
        nickname = data.get('nickname')
        email = data.get("email")
        about = data.get('about')
        assert username is not None
        assert avatar is not None
        assert nickname is not None
        assert email is not None
        assert about is not None

    def test_change_user_info(self, client):
        global user
        user['password'] = 'password_new'
        res = client.put(url_for('admin.user_info_view'), json=user, headers=headers)
        assert b'success' in res.data

    def test_logout(self, client):
        res = client.delete(
            url_for('admin.logout_view'),
            headers=headers
        )
        assert b'success' in res.data

    def test_after_logout_auth(self, client):
        res = client.get(url_for('admin.auth_view'), headers=headers)
        assert b'success' not in res.data
