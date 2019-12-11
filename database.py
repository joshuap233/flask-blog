from . import db

tags_to_post = db.Table(
    'tags_to_post',
    db.Column('tags_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True),
    db.Column('post_id', db.Integer, db.ForeignKey('post.id'), primary_key=True)
)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_title = db.Column(db.String(128), unique=True, index=True)
    post_contents = db.Column(db.Text, nullable=True)
    post_date = db.Column(db.BigInteger)
    post_publish = db.Column(db.Boolean, nullable=False, default=False)
    tags = db.relationship('Tag', secondary=tags_to_post, backref=db.backref('posts', lazy='dynamic'))
    urls = db.relationship('Url', backref='post', lazy='dynamic')

    def __init__(self, title, contents, date, publish: bool):
        self.post_title = title,
        self.post_contents = contents,
        self.post_date = date,
        self.post_publish = publish


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tag_name = db.Column(db.String(64), unique=True, index=True)

    def __init__(self, tag):
        self.tag_name = tag


# 储存文章图片url与图片名映射
class Url(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.String(64), db.ForeignKey('post.id'))
    path = db.Column(db.String(64))
    file_name = db.Column(db.String(128))


class User(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    user_about = db.Column(db.Text)

    def __init__(self, about):
        self.user_about = about
