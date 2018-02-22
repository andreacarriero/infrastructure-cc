from toolbox.database import db
from modules.user.models import User

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.ForeignKey(User.id))
    name = db.Column(db.String(100))

    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name
        }