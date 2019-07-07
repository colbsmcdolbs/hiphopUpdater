from app import db


class Rapper(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)

    def __repr__(self):
        return '<Rapper {}>'.format(self.name)


class signed_up(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rapper_id = db.Column(db.Integer, index=True)
    email = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        return '<signed_up {}>'.format(self.email)
