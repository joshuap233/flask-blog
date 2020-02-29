from app.model.db import User, db

uid = ''


def test_set_password():
    with db.auto_commit():
        user = User(email='101242@gmail.com', email_is_validate=True)
        user.set_password('password')
        db.session.add(user)
    user.check_password('password')
    global uid
    uid = user.id


def test_set_code():
    code = User.set_code_by(uid=uid)
    User.validate_code({
        'email': '101242@gmail.com',
        'code': code
    })
