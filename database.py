from . import db

tag_to_post = db.Table(
    'tag_to_post',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
    db.Column('post_id', db.Integer, db.ForeignKey('post.id'))
)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_title = db.Column(db.String(128), unique=True)
    post_contents = db.Column(db.Text, nullable=True)
    post_date = db.Column(db.BigInteger)
    post_publish = db.Column(db.Boolean, nullable=False, default=False)
    tag = db.relationship('Tag', secondary=tag_to_post, backref=db.backref('post', lazy='dynamic'))

    def __init__(self, title, contents, date, publish: bool,tags):
        self.post_title = title,
        self.post_contents = contents,
        self.post_date = date,
        self.post_publish = publish
        self.tag = tags


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tag_name = db.Column(db.String(64), unique=True)

    def __init__(self, name):
        self.tag_name = name


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_about = db.Column(db.Text)

    def __init__(self, about):
        self.user_about = about
