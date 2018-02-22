from toolbox.database import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)

    def serialize(self):
        return {
            'id': self.id,
            'username': self.username
        }
