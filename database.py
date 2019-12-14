from werkzeug.security import check_password_hash, generate_password_hash

from . import db, login_manager

tags_to_post = db.Table(
    'tags_to_post',
    db.Column('tags_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True),
    db.Column('post_id', db.Integer, db.ForeignKey('post.id'), primary_key=True)
)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_title = db.Column(db.String(128), unique=True, index=True)
    post_contents = db.Column(db.Text, nullable=True)
    post_date = db.Column(db.BigInteger, index=True)
    post_change_date = db.Column(db.BigInteger, index=True)
    post_publish = db.Column(db.Boolean, nullable=False, default=False)
    tags = db.relationship('Tag', secondary=tags_to_post, backref=db.backref('posts', lazy='dynamic'))

    def __init__(self, title, contents, date, publish=False):
        self.post_title = title,
        self.post_contents = contents,
        self.post_date = date,
        self.post_change_date = date,
        self.post_publish = publish


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tag_name = db.Column(db.String(64), unique=True, index=True)

    def __init__(self, tag):
        self.tag_name = tag


class User(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    nickname = db.Column(db.String(128))
    username = db.Column(db.String(128))
    email = db.Column(db.String(128))
    phone = db.Column(db.String(32))
    password_hash = db.Column(db.String(128))
    user_about = db.Column(db.Text)

    def generate_password_hash(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login_manager.user_loader
def load_user(uid):
    return User.get(uid)
