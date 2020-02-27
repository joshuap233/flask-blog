from flask import url_for, current_app


# def test_login_auth_logout(client):
#     user = {
#         'username': 'username',
#         'password': 'password'
#     }
#     # 测试登录
#     res = client.post(url_for('admin.login_view'), json=user)
#     data = res.get_json().get('data')
#     token = data.get('token')
#     id_ = data.get('id')
#     assert b'success' in res.data
#     assert token is not None
#
#     headers = {
#         'identify': id_,
#         'Authorization': f'Bearer {token}'
#     }
#
#     # 测试身份验证
#     res = client.get(
#         url_for('admin.auth_view'),
#         headers=headers
#     )
#     assert b'success' in res.data
#
#     # 测试登出
#     res = client.get(url_for('admin.logout_view'), headers=headers)
#     assert b'success' in res.data
#
#     # 登出后测试身份验证
#     res = client.get(url_for('admin.auth_view'), headers=headers)
#     assert b'failed' in res.data


def test_generate_confirm_token(client):
    res = client.get(url_for('admin.generate_token'))
    data = res.get_json().get('data')
    token = data.get('token')
    assert token is not None

    res = client.get(url_for('admin.auth_token', token=token))
    assert b'success' in res.data
