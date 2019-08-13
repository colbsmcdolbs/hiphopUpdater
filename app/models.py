from app import db


class Rapper(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)

    def __repr__(self):
        return '{}'.format(self.name)

    def __unicode__(self):
        return self.name


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rapper_id = db.Column(db.Integer, index=True, nullable=False)
    email = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        return '<User {}>'.format(self.email)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        return '<Post {}>'.format(self.post_id)


def import_user(user_email, user_rapper_id):
    try:
        user = User(email=user_email, rapper_id=user_rapper_id)
        db.session.add(user)
        db.session.commit()
    except:
        db.session.rollback()


def import_post(user_post_id):
    try:
        post = Post(post_id=user_post_id)
        db.session.add(post)
        db.session.commit()
    except:
        db.session.rollback()


def delete_user(user_email):
    if User.query.filter_by(email=user_email).first():
        User.query.filter_by(email=user_email).delete()
        db.session.commit()


def clear_posts():
    try:
        Post.query.delete()
        db.session.commit()
    except:
        db.session.rollback()
