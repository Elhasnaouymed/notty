from typing import Union

from flask import Flask, Blueprint
from flask_restful import Api, marshal_with

api = Api(prefix='/api')


def marshal_return(r, fields: dict):
    """
    Instead of using marshal_with as a decorator on your resource endpoints,
    you can use this on the return statement (more control of what you want to use
    """
    return marshal_with(fields)(lambda: r)()


def init_api(app: Union[Flask, Blueprint]):
    from .user_resource import UserResource
    from .note_resource import NoteResource
    api.add_resource(UserResource, '/user')
    api.add_resource(NoteResource, '/note')
    api.init_app(app)
