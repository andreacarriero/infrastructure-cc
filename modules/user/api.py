import logging
from flask import Blueprint, abort
from flask_restful import Api, Resource, reqparse

from toolbox.logger import get_logger
from modules.user.models import User

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

api.add_resource(RootResource, '/', endpoint='users')
