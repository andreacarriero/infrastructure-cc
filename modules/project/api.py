import logging
from flask import Blueprint, abort
from flask_restful import Api, Resource, reqparse

from toolbox.logger import get_logger
from modules.project.models import Project

log = get_logger(__name__)

app = Blueprint(__name__, __name__)
api = Api(app)

class RootResource(Resource):
    """
    Manages Projects
    """

    def get(self):
        log.info("Getting all projects")
        projects = Project.query.all()
        return [project.serialize() for project in projects]

api.add_resource(RootResource, '/', endpoint='projects')
