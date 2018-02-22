from toolbox.database import db

class Datacenter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True)
    location = db.Column(db.String(20))
    latitude = db.Column(db.String(20))
    longitude = db.Column(db.String(20))

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'location': self.location,
            'latitude': self.latitude,
            'longitude': self.longitude
        }        