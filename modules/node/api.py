import logging
from flask import Blueprint, abort
from flask_restful import Api, Resource, reqparse

from toolbox.logger import get_logger
from toolbox.database import db
from modules.node.models import Node, NodeIP, NodeCommand
from modules.datacenter.models import Datacenter
from modules.project.models import Project, ResourceNodeLink, ProjectCommandJob

log = get_logger(__name__)

app = Blueprint(__name__, __name__)
api = Api(app)

class RootResource(Resource):
    """
    Manages Nodes
    """

    def get(self):
        log.info("Getting all nodes")
        nodes = Node.query.all()
        return [node.serialize() for node in nodes]

class IPsResource(Resource):
    """
    Manages IPs
    """

    def get(self):
        log.info("Getting all IPs")
        ips = NodeIP.query.all()
        return [ip.serialize() for ip in ips]

class NodeResource(Resource):
    """
    Manages specific node
    """

    def get(self, node_id):
        log.info("Getting node ID:%d", node_id)

        node = Node.query.filter_by(id=node_id).first()
        if not node:
            abort(404)

        datacenter = Datacenter.query.filter_by(id=node.datacenter_id).first()
        resource_links = ResourceNodeLink.query.filter_by(node_id=node_id).all() 

        return {
            'node': node.serialize(),
            'datacenter': datacenter.serialize(),
            'hosted_projects': [link.serialize_project() for link in resource_links]
        }

class NodeCommandsResource(Resource):
    """
    Manages node commands
    """

    def get(self, node_id):
        log.info("Getting commands for node ID:%s", node_id)
        node = Node.query.filter_by(id=node_id).first()
        if not node:
            abort(404)
        
        commands = NodeCommand.query.filter_by(node_id=node_id).all()

        return [command.serialize() for command in commands]

class NodeCommandResource(Resource):
    """
    Manages node command
    """

    def get(self, node_id, command_id):
        log.info("Getting command ID:%d for node ID:%d", command_id, node_id)
        
        node = Node.query.filter_by(id=node_id).first()
        if not node:
            abort(404, "Node not found")
        
        command = NodeCommand.query.filter_by(id=command_id).first()
        if not command:
            abort(404, "Command not found")

        project_command_job = ProjectCommandJob.query.filter_by(id=command.project_command_job_id).first()
        if not project_command_job:
            abort(404, "Project Command Job not found")

        return {
            'node': node.serialize(),
            'command': command.serialize(),
            'project_command_job': project_command_job.serialize()
        }

    def post(self, node_id, command_id):
        log.info("Setting data for command ID:%d on node ID:%d", command_id, node_id)

        parser = reqparse.RequestParser()
        parser.add_argument('status', type=str)
        parser.add_argument('response', type=str)
        args = parser.parse_args()

        node = Node.query.filter_by(id=node_id).first()
        if not node:
            abort(404, "Node not found")

        command = NodeCommand.query.filter_by(id=command_id).first()
        if not command:
            abort(404, "Command not found")
        
        if args.get('status'):
            command.status = args.get('status')

        if args.get('response'):
            command.response = args.get('response')

        db.session.commit()

        return self.get(node_id, command_id)

api.add_resource(RootResource, '/', endpoint='nodes')
api.add_resource(NodeResource, '/<int:node_id>', endpoint='node')
api.add_resource(NodeCommandsResource, '/<int:node_id>/commands/', endpoint='node_commands')
api.add_resource(NodeCommandResource, '/<int:node_id>/commands/<int:command_id>', endpoint='node_command')
api.add_resource(IPsResource, '/ips/', endpoint='ips')