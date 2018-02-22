from toolbox.database import db

from modules.datacenter.models import Datacenter

class Node(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    type = db.Column(db.String(20))
    datacenter_id = db.Column(db.ForeignKey(Datacenter.id))

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type,
            'datacenter_id': self.datacenter_id
        }

class NodeIP(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    node_id = db.Column(db.ForeignKey(Node.id))
    ipv = db.Column(db.Integer)
    ip = db.Column(db.String(46))
    netmask = db.Column(db.Integer)

    def serialize(self):
        return {
            'id': self.id,
            'node_id': self.node_id,
            'ipv': self.ipv,
            'ip': self.ip,
            'netmask': self.netmask
        }