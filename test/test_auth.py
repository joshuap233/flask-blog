from faker import Faker
from flask import url_for
from app.model.db import User, db
from app.utils import get_attr

faker = Faker('zh_CN')
user = {
    'username': faker.name(),
    'nickname': faker.name(),
    'password': 'password123',
    'confirm_password': 'password123',
    'email': 'aaaa@qq.com'
}

headers = {
    'identify': '',
    'Authorization': ''
}


class TestUser(object):
    def test_delete_user(self, client, app):
        with app.app_context():
            user = User.query.first()
            db.session.delete(user)
            db.session.commit()

    # 测试注册
    def test_register(self, client):
        res = client.post(
            url_for('admin.register_view'),
            json=user
        )
        assert b'success' in res.data

    def test_login(self, client):
        res = client.post(
            url_for('admin.login_view'),
            json=user
        )
        assert b'success' in res.data
        data = res.get_json().get('data')
        id_ = data.get('id')
        token = data.get('token')
        assert id_ is not None
        assert token is not None
        headers['identify'] = id_
        headers['Authorization'] = f'Bearer {token}'

    def test_auth(self, client):
        res = client.get(url_for('admin.auth_view'), headers=headers)
        assert b'success' in res.data

    def test_user_info_without_auth_header(self, client):
        res = client.get(url_for('admin.user_info_view'))
        assert b'failed' in res.data

    def test_get_user_info(self, client):
        res = client.get(url_for('admin.user_info_view'), headers=headers)
        assert b'success' in res.data
        data = res.get_json().get('data')
        res: list = get_attr(['username', 'avatar', 'nickname', 'email', 'about'], data)
        for item in res:
            assert item is not None

    def test_change_user_info(self, client):
        u = user.copy()
        u['password'] = 'password_new',
        res = client.patch(
            url_for('admin.user_info_view'),
            json=u, headers=headers
        )
        assert b'success' in res.data

    def test_reset_email(self, client):
        res = client.get(
            url_for('admin.email_view'),
            headers=headers
        )
        assert b'success' in res.data
        u = User.search_by(email=user['email'])
        code = u.code.code
        new_email = 'bbbb@qq.com'
        user['email'] = new_email
        res = client.put(
            url_for('admin.email_view'),
            json=dict(
                email=new_email,
                code=code
            ),
            headers=headers
        )
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

    def test_forget_password(self, client):
        res = client.get(
            url_for('admin.recovery_password_view', email=user['email']),
        )
        assert b'success' in res.data
        u = User.search_by(email=user['email'])
        res = client.put(
            url_for('admin.recovery_password_view'),
            json={
                'email': user['email'],
                'code': u.code.code,
                'password': 'new_password',
                'confirm_password': 'new_password',
            },
        )
        assert b'success' in res.data
