import logging
from flask import Blueprint, abort
from flask_restful import Api, Resource, reqparse

from toolbox.logger import get_logger
from modules.datacenter.models import Datacenter

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

api.add_resource(RootResource, '/', endpoint='datacenters')