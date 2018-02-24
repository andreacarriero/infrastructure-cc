from sqlalchemy import desc
import datetime

from toolbox.database import db

from modules.datacenter.models import Datacenter

class Node(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    type = db.Column(db.String(20))
    datacenter_id = db.Column(db.ForeignKey(Datacenter.id))

    def __init__(self, name, type, datacenter_id):
        self.name = name
        self.type = type

        datacenter = Datacenter.query.filter_by(id=datacenter_id).first()
        if not datacenter:
            raise ValueError("Datacenter with id %d does not exist" % datacenter_id)
        self.datacenter_id = datacenter_id

    def create(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get(id):
        return Node.query.filter_by(id=id).first()

    def serialize(self):
        ips = NodeIP.query.filter_by(node_id = self.id).all()
        status = NodeStatus.query.filter_by(node_id = self.id).order_by(desc(NodeStatus.last_update)).first()

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
    STATUS_ONLINE = 'online'
    STATUS_OFFLINE = 'offline'

    id = db.Column(db.Integer, primary_key=True)
    node_id = db.Column(db.ForeignKey(Node.id))
    last_update = db.Column(db.DateTime, default=datetime.datetime.now())
    imposed_status = db.Column(db.String(20))
    current_status = db.Column(db.String(20))

    def __init__(self, node_id, imposed_status):
        self.node_id = node_id
        self.imposed_status = imposed_status

    def create(self):
        db.session.add(self)
        db.session.commit()

    def serialize(self):
        return {
            'id': self.id,
            'node_id': self.node_id,
            'last_update': str(self.last_update),
            'imposed_status': self.imposed_status,
            'current_status': self.current_status
        }

class NodeCommand(db.Model):
    from modules.project.models import ProjectCommandJob

    STATUS_SENDING = 'sending'
    STATUS_RECEIVED = 'received'
    STATUS_PENDING = 'pending'
    STATUS_COMPLETED = 'completed'
    STATUS_ERROR = 'error'
    STATUS_FAILED = 'failed'

    id = db.Column(db.Integer, primary_key=True)
    add_date = db.Column(db.DateTime, default=datetime.datetime.now())
    node_id = db.Column(db.ForeignKey(Node.id))
    project_command_job_id = db.Column(db.ForeignKey(ProjectCommandJob.id))
    response = db.Column(db.String(5000))
    status = db.Column(db.String(100), default=STATUS_SENDING)

    def serialize(self):
        return {
            'id': self.id,
            'add_date': str(self.add_date),
            'node_id': self.node_id,
            'project_command_job_id': self.project_command_job_id,
            'response': self.response,
            'status': self.status
        }
