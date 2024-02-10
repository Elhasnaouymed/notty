from typing import Union

from flask import Flask, Blueprint
from flask_restx import Api

from ..constants import SCodes

api = Api(prefix='/api/', doc='/api/', version='0.1', title='Notty Official RestX API', description='Allows you to create and manage everything through the RESTX API.')


def _init_error_handlers(api_: Api):
    # > handling Exception make it reformat any error message into response by stringify-ing the error
    @api_.errorhandler(Exception)
    def handle_root_exception(error):
        return {'message': str(error)}, SCodes.BAD_REQUEST_400


def init_api(app: Union[Flask, Blueprint]):
    """
    **API Initialization Method**

    This method registers the API resources (routes) in the API,
    and initializes the API with Flask app
    :param app: Flask
    :return: RestX API Object
    """
    from .user_resource import user_namespace
    from .note_resource import note_namespace
    api.add_namespace(user_namespace)
    api.add_namespace(note_namespace)
    app.logger.debug('Done: API resources added.')

    _init_error_handlers(api)

    api.init_app(app)
    app.logger.debug('Done: API initialized.')

    return api
