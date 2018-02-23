import datetime
from toolbox.database import db
from modules.user.models import User
from modules.node.models import Node

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.ForeignKey(User.id))
    name = db.Column(db.String(100))

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
    add_date = db.Column(db.DateTime, server_default=db.func.now())
    project_id = db.Column(db.ForeignKey(Project.id))
    propagated = db.Column(db.Boolean, default=False)
    propagation_date = db.Column(db.DateTime)
    cmd = db.Column(db.String(5000))

    def serialize(self):
        return {
            'id': self.id,
            'add_date': str(self.time),
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
