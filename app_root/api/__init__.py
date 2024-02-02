from typing import Union

from flask import Flask, Blueprint
from flask_restx import Api


def init_api(app: Union[Flask, Blueprint]):
    """
    **API Factory Method**

    This method registers the API resources (routes) in our API,
    and initializes the API with Flask app
    :param app: Flask
    :return: new RestX API
    """
    api = Api(prefix='/api', doc=False)
    app.logger.debug('Done: API created.')

    from .user_resource import UserResource
    from .note_resource import NoteResource
    api.add_resource(UserResource, '/user')
    api.add_resource(NoteResource, '/note')
    app.logger.debug('Done: API resources added.')

    api.init_app(app)
    app.logger.debug('Done: API initialized.')
