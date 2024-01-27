from flask_restful import Resource, fields, reqparse, request

from . import marshal_return
from ..constants import SCodes


# > marshaling NoteModel
note_model_fields = {
    'id': fields.Integer(),
    'title': fields.String(),
    'content': fields.String(),
    'create_date': fields.DateTime(),
    'last_modified': fields.DateTime(),
    'user_id': fields.Integer(),
    'username': fields.String(attribute='user.username'),
}


# > used in NoteResource.post endpoint
note_post_args_parser = reqparse.RequestParser()
note_post_args_parser.add_argument('title', type=str)
note_post_args_parser.add_argument('content', type=str)
note_post_args_parser.add_argument('user_id', type=int)
note_post_args_parser.add_argument('username', type=str)


# used in NoteResource.delete endpoint
note_delete_args_parser = reqparse.RequestParser()
note_delete_args_parser.add_argument('id', type=int)


class NoteResource(Resource):
    def get(self):
        try:
            args = request.args
            arg_id = args.get('id')
            arg_id = int(arg_id)
        except Exception as ex:
            return {'message': 'Argument error!'}, SCodes.BAD_REQUEST_400

        from ..models import DatabaseSimpleAPI
        dsi = DatabaseSimpleAPI()

        note = dsi.get_note(arg_id)
        if note is None:
            return {'message': 'Note not found'}, SCodes.NOT_FOUND_404
        return marshal_return(note, note_model_fields)

    def post(self):
        try:
            args = note_post_args_parser.parse_args()
            arg_title = args.get('title')
            arg_content = args.get('content')
            arg_user_id = args.get('user_id')
            arg_user_id = int(arg_user_id) if arg_user_id else None
            arg_username = args.get('username')
            user_identifier = arg_user_id if arg_user_id else arg_username
            assert user_identifier is not None
        except Exception as ex:
            return {'message': 'Argument error!'}, SCodes.BAD_REQUEST_400

        from ..models import DatabaseSimpleAPI
        dsi = DatabaseSimpleAPI(True)

        try:
            new_note = dsi.add_note(title=arg_title, content=arg_content, user=user_identifier)
        except Exception as ex:
            return {'message': str(ex)}, SCodes.BAD_REQUEST_400

        return {'success': 'Note added!', 'note_id': new_note.id}, SCodes.OK_200

    def delete(self):
        try:
            args = note_delete_args_parser.parse_args()
            note_id = int(args.get('id'))
        except Exception as ex:
            return {'message': 'Argument Error!'}, SCodes.BAD_REQUEST_400

        from ..models import DatabaseSimpleAPI
        dsi = DatabaseSimpleAPI(True)
        try:
            dsi.delete_note(note_id)
        except Exception as ex:
            return {'message': str(ex)}
        return {'success': 'Note has been deleted!'}, SCodes.OK_200
