import logging
from flask import Blueprint, abort
from flask_restful import Api, Resource, reqparse

from toolbox.logger import get_logger
from modules.node.models import Node

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

api.add_resource(RootResource, '/', endpoint='nodes')