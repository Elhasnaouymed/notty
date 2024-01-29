from flask_restx import Resource, fields, reqparse
from flask import request

from .utils import marshal_return
from ..constants import SCodes


# > marshaling UserModel
user_model_fields = {
    'id': fields.Integer(),
    'username': fields.String(),
    'join': fields.DateTime(),
    'token': fields.String(),
}

# > used in UserResource.post endpoint
user_post_args_parser = reqparse.RequestParser()
user_post_args_parser.add_argument('username', type=str, required=True)
user_post_args_parser.add_argument('password', type=str, required=True)

# > used in UserResource.delete endpoint
user_delete_args_parser = reqparse.RequestParser()
user_delete_args_parser.add_argument('id', type=int)
user_delete_args_parser.add_argument('username', type=str)


class UserResource(Resource):
    def get(self):
        # > process args
        try:
            args = request.args
            arg_id = args.get('id')
            arg_username = args.get('username')
            arg_id = int(arg_id) if arg_id else None
        except Exception as ex:
            return {'message': 'Arguments Error!'}, SCodes.BAD_REQUEST_400

        from ..models import DatabaseSimpleAPI
        dsi = DatabaseSimpleAPI()

        user = dsi.get_user(arg_id if arg_id else arg_username)
        if user is None:
            return {'message': 'User not found!'}, SCodes.NOT_FOUND_404
        return marshal_return(user, user_model_fields)

    def post(self):
        try:
            args = user_post_args_parser.parse_args()
            arg_username = args.get('arg_username')
            arg_password = args.get('password')
        except Exception as ex:
            return {'message': 'Arguments Error!'}, SCodes.BAD_REQUEST_400

        from ..models import DatabaseSimpleAPI
        dsa = DatabaseSimpleAPI(True)

        new_user = dsa.add_user(arg_username, arg_password)
        return {'success': 'User Added!', 'user_id': new_user.id}, SCodes.OK_200

    def delete(self):
        try:
            args = user_delete_args_parser.parse_args()
            arg_id = args.get('id')
            arg_username = args.get('username')
            assert not (arg_id is arg_username is None)  # - when no argument was passed, error
        except Exception as ex:
            return {'message': 'Arguments Error!'}, SCodes.BAD_REQUEST_400

        from ..models import DatabaseSimpleAPI
        dsa = DatabaseSimpleAPI(True)

        user = arg_id if arg_id else arg_username
        try:
            dsa.delete_user(user)
        except Exception as ex:
            return {'message': str(ex)}
        return {'success': 'User deleted!'}, SCodes.OK_200
