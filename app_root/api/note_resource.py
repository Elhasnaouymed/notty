from flask_restx import Resource, fields, reqparse, Namespace, marshal_with
from flask import request

from .api_models import *
from ..constants import SCodes
from .. import exceptions as excs


note_namespace = Namespace('Note', path='/note', description='Create and manage Notes')


@note_namespace.route('/')
class NoteResource(Resource):
    @marshal_with(note_model)
    @note_namespace.expect(note_get_parser)
    def get(self):
        arg_id = note_get_parser.parse_args().get('id')
        from ..models import DatabaseSimpleAPI
        dsi = DatabaseSimpleAPI()

        note = dsi.get_note(arg_id)
        if note is None:
            raise excs.NoteNotFoundError(arg_id)
        return note

    @note_namespace.expect(note_post_model)
    @marshal_with(note_model)
    def post(self):
        payload = note_namespace.payload
        arg_title = payload.get('title')
        arg_content = payload.get('content')
        arg_user_id = payload['user'].get('id')
        arg_user_name = payload['user'].get('username')
        user_identifier = arg_user_id if arg_user_id else arg_user_name

        from ..models import DatabaseSimpleAPI
        dsi = DatabaseSimpleAPI(True)

        new_note = dsi.add_note(title=arg_title, content=arg_content, user=user_identifier)
        return new_note, SCodes.CREATED_201

    @note_namespace.expect(note_delete_model)
    def delete(self):
        arg_id = note_namespace.payload.get('id')

        from ..models import DatabaseSimpleAPI
        dsi = DatabaseSimpleAPI(True)
        dsi.delete_note(arg_id)
        return {'success': 'Note has been deleted!'}, SCodes.OK_200
