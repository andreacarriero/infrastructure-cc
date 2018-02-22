import logging
from flask import Blueprint, abort
from flask_restful import Api, Resource, reqparse

from toolbox.logger import get_logger
from modules.user.models import User
from modules.project.models import Project

log = get_logger(__name__)

app = Blueprint(__name__, __name__)
api = Api(app)

class RootResource(Resource):
    """
    Manages Users
    """

    def get(self):
        log.info("Getting all users")
        users = User.query.all()
        return [user.serialize() for user in users]

class UserResource(Resource):
    """
    Manages specific user
    """

    def get(self, user_id):
        user = User.query.filter_by(id=user_id).first()
        if not user:
            abort(404)
        
        projects = Project.query.filter_by(user_id=user_id).all()

        return {
            'user': user.serialize(),
            'projects': [project.serialize() for project in projects]
        }

api.add_resource(RootResource, '/', endpoint='users')
api.add_resource(UserResource, '/<int:user_id>', endpoint='user')
