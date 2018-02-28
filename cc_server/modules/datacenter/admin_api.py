import logging
from flask import Blueprint, abort
from flask_restful import Api, Resource, reqparse

from toolbox.logger import get_logger
from modules.datacenter.models import Datacenter
from modules.node.models import Node

log = get_logger(__name__)

app = Blueprint(__name__, __name__)
api = Api(app)

class RootResource(Resource):
    """
    Manages DCs
    """

    def get(self):
        log.info("Getting all datacenters")
        datacenters = Datacenter.query.all()
        return [datacenter.serialize() for datacenter in datacenters]

class DatacenterResource(Resource):
    """
    Manages specific datacenter
    """
    
    def get(self, datacenter_id):
        log.info("Getting datacenter ID:%d", datacenter_id)
        datacenter = Datacenter.query.filter_by(id=datacenter_id).first()
        if not datacenter:
            abort(404)
        
        dc_nodes = Node.query.filter_by(datacenter_id=datacenter_id).all()

        return {
            'datacenter': datacenter.serialize(),
            'nodes': [node.serialize() for node in dc_nodes]
        }

api.add_resource(RootResource, '/', endpoint='datacenters')
api.add_resource(DatacenterResource, '/<int:datacenter_id>', endpoint='datacenter')