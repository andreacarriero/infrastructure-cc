import datetime
from toolbox.database import db
from modules.user.models import User
from modules.node.models import Node

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.ForeignKey(User.id))
    name = db.Column(db.String(100))

    def __init__(self, user_id, name):
        self.user_id = user_id
        self.name = name

    def create(self):
        db.session.add(self)
        db.session.commit()

    def add_node(self, node_id):
        node = Node.get(node_id)
        if not node:
            raise ValueError("Node with id %d does not exist" % node_id)

        link = ResourceNodeLink(self.id, node_id)
        link.create()

    @staticmethod
    def get(id):
        return Project.query.filter_by(id=id).first()

    def serialize(self):
        nodes_links = ResourceNodeLink.query.filter_by(project_id=self.id).all()

        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'nodes_ids': [link.node_id for link in nodes_links]
        }

class ResourceNodeLink(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.ForeignKey(Project.id))
    node_id = db.Column(db.ForeignKey(Node.id))

    def __init__(self, project_id, node_id):
        project = Project.get(project_id)
        if not project:
            raise ValueError("Project with id %d does not exist" % project_id)

        node = Node.get(node_id)
        if not node:
            raise ValueError("Node with id %d does not exist" % node_id)

        self.project_id = project_id
        self.node_id = node_id

    def create(self):
        db.session.add(self)
        db.session.commit()

    def serialize(self):
        return {
            'id': self.id,
            'project_id': self.project_id,
            'node_id': self.node_id
        }
    
    def serialize_node(self):
        node = Node.query.filter_by(id=self.node_id).first()
        return node.serialize()

    def get_node(self):
        node = Node.query.filter_by(id=self.node_id).first()
        return node

    def serialize_project(self):
        project = Project.query.filter_by(id=self.project_id).first()
        return project.serialize()

    def get_project(self):
        project = Project.query.filter_by(id=self.project_id).first()
        return project

class ProjectCommandJob(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    add_date = db.Column(db.DateTime, default=datetime.datetime.now())
    project_id = db.Column(db.ForeignKey(Project.id))
    propagated = db.Column(db.Boolean, default=False)
    propagation_date = db.Column(db.DateTime)
    cmd = db.Column(db.String(5000))

    def __init__(self, project_id, cmd):
        project = Project.get(project_id)
        if not project:
            raise ValueError("Project with id %d does not exist" % project_id)
        self.project_id = project_id
        self.cmd = cmd

    def create(self):
        db.session.add(self)
        db.session.commit()

    def serialize(self):
        return {
            'id': self.id,
            'add_date': str(self.add_date),
            'project_id': self.project_id,
            'propagated': self.propagated,
            'propagation_date': str(self.propagation_date),
            'cmd': self.cmd
        }

    def propagate(self):
        from modules.node.models import NodeCommand

        project = Project.query.filter_by(id=self.project_id).first()
        nodes_links = ResourceNodeLink.query.filter_by(project_id=self.project_id).all()
        nodes = [link.get_node() for link in nodes_links]

        for node in nodes:
            node_command = NodeCommand()
            node_command.node_id = node.id
            node_command.project_command_job_id = self.id
            db.session.add(node_command)

        self.propagated = True
        self.propagation_date = datetime.datetime.now()
        db.session.commit()
