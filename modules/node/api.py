import logging
from flask import Blueprint, abort
from flask_restful import Api, Resource, reqparse

from toolbox.logger import get_logger
from modules.node.models import Node, NodeIP
from modules.datacenter.models import Datacenter
from modules.project.models import Project, ResourceNodeLink

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

api.add_resource(RootResource, '/', endpoint='nodes')
api.add_resource(NodeResource, '/<int:node_id>', endpoint='node')
api.add_resource(IPsResource, '/ips/', endpoint='ips')
