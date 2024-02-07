from flask_restx import Resource, fields, reqparse, Namespace, marshal_with
from flask import request

from .api_models import *
from ..constants import SCodes
from .. import exceptions as excs


user_namespace = Namespace('User', path='/user', description='Create and manage Users')


@user_namespace.route('/')
class UserResource(Resource):
    @user_namespace.expect(user_get_parser)
    @user_namespace.marshal_with(user_model)
    def get(self):
        args = user_get_parser.parse_args()
        arg_id = args.get('id')
        arg_username = args.get('username')

        from ..models import DatabaseSimpleAPI
        dsi = DatabaseSimpleAPI()

        user_identifier = arg_id if arg_id else arg_username
        user = dsi.get_user(user_identifier)
        if not user:
            raise excs.UserNotFoundError(user_identifier)
        return user

    @user_namespace.expect(user_post_fields)
    @user_namespace.marshal_with(user_model)
    def post(self):
        arg_username = user_namespace.payload.get('username')
        arg_password = user_namespace.payload.get('password')
        if not arg_password:
            raise excs.WeakPasswordError()

        from ..models import DatabaseSimpleAPI
        dsa = DatabaseSimpleAPI(True)

        new_user = dsa.add_user(arg_username, arg_password)
        return new_user, SCodes.CREATED_201

    @user_namespace.expect(user_delete_fields)
    def delete(self):
        arg_id = user_namespace.payload.get('id')
        arg_username = user_namespace.payload.get('username')

        from ..models import DatabaseSimpleAPI
        dsa = DatabaseSimpleAPI(True)

        user = arg_id if arg_id else arg_username
        dsa.delete_user(user)
        return {'success': 'User deleted!'}, SCodes.OK_200
