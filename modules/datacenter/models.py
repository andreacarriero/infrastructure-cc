from toolbox.database import db

class Datacenter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True)
    location = db.Column(db.String(20))
    latitude = db.Column(db.String(20))
    longitude = db.Column(db.String(20))

    def __init__(self, name, location):
        self.name = name
        self.location = location

    def create(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get(id):
        return Datacenter.query.filter_by(id=id).first()

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'location': self.location,
            'latitude': self.latitude,
            'longitude': self.longitude
        }        