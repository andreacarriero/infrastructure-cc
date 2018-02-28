from toolbox.database import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)

    def __init__(self, username):
        self.username = username

    def create(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get(id):
        return User.query.filter_by(id=id).first()

    def serialize(self):
        return {
            'id': self.id,
            'username': self.username
        }
