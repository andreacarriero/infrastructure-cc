import logging
from flask import Blueprint, abort
from flask_restful import Api, Resource, reqparse

from toolbox.logger import get_logger
from modules.project.models import Project, ResourceNodeLink, ProjectCommandJob
from modules.user.models import User
from modules.node.models import Node

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

class ProjectResource(Resource):
    """
    Manages specific project
    """

    def get(self, project_id):
        log.info("Getting project ID:%d", project_id)

        project = Project.query.filter_by(id=project_id).first()
        if not project:
            abort(404)

        user = User.query.filter_by(id=project.user_id).first()
        nodes_links = ResourceNodeLink.query.filter_by(project_id=project_id).all()
        project_command_jobs = ProjectCommandJob.query.filter_by(project_id=project_id).all()

        return {
            'project': project.serialize(),
            'user': user.serialize(),
            'nodes': [link.serialize_node() for link in nodes_links],
            'project_command_jobs': [job.serialize() for job in project_command_jobs]
        }

api.add_resource(RootResource, '/', endpoint='projects')
api.add_resource(ProjectResource, '/<int:project_id>', endpoint='project')
