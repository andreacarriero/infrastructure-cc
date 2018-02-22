from toolbox.database import db

from modules.datacenter.models import Datacenter

class Node(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    type = db.Column(db.String(20))
    datacenter_id = db.Column(db.ForeignKey(Datacenter.id))

    def serialize(self):
        ips = NodeIP.query.filter_by(node_id = self.id).all()
        status = NodeStatus.query.filter_by(node_id = self.id).order_by('-last_update').first()

        return {
            'id': self.id,
            'name': self.name,
            'type': self.type,
            'datacenter_id': self.datacenter_id,
            'ips': [ip.serialize() for ip in ips],
            'status': (lambda status: status.serialize() if status else None)(status)
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

class NodeStatus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    node_id = db.Column(db.ForeignKey(Node.id))
    last_update = db.Column(db.DateTime, server_default=db.func.now())
    imposed_status = db.Column(db.String(20))
    current_status = db.Column(db.String(20))

    def serialize(self):
        return {
            'id': self.id,
            'node_id': self.node_id,
            'last_update': str(self.last_update),
            'imposed_status': self.imposed_status,
            'current_status': self.current_status
        }