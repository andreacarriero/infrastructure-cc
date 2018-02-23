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

    def serialize_project(self):
        project = Project.query.filter_by(id=self.project_id).first()
        return project.serialize()

class ProjectCommandJob(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime, server_default=db.func.now())
    project_id = db.Column(db.ForeignKey(Project.id))
    cmd = db.Column(db.String(5000))

    def serialize(self):
        return {
            'id': self.id,
            'time': str(self.time),
            'project_id': self.project_id,
            'cmd': self.cmd
        }

    def propagate(self):
        from modules.node.models import NodeCommand
        
        project = Project.query.filter_by(id=self.project_id).first()
        nodes = [Node.query.filter_by(id=node_id) for node_id in project.nodes_ids]
        for node in nodes:
            node_command = NodeCommand()
            node_command.node_id = node.id
            node_command.project_command_job_id = self.id
            db.session.add(node_command)
        db.session.commit()
