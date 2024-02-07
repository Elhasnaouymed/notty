from flask_restx import fields, reqparse

from . import api

# > used to marshal the user.get route
user_model = api.model('User Model', {
    'id': fields.Integer(),
    'username': fields.String(),
    'join': fields.DateTime(),
    'token': fields.String(),
})

# > used only as a nested field in note_post_model
user_get_model = api.model('User Get Model', {
    'id': fields.Integer(),
    'username': fields.String()
})

# > used to parse URL parameters in user.get
user_get_parser = reqparse.RequestParser()
user_get_parser.add_argument('id', type=int, help="The User's id")
user_get_parser.add_argument('username', type=str, help="The User's username")

# > post fields in user.post
user_post_fields = api.model('User Post Model', {
    'username': fields.String(),
    'password': fields.String()
})

# > to delete a user (by id or username), user.delete
user_delete_fields = api.model('User Delete Model', {
    'id': fields.Integer(),
    'username': fields.String()
})


note_model = api.model('Note Model', {
    'id': fields.Integer(),
    'title': fields.String(),
    'content': fields.String(),
    'create_date': fields.DateTime(),
    'last_modified': fields.DateTime(),
    'user': fields.Nested(user_model),
})

note_get_parser = reqparse.RequestParser()
note_get_parser.add_argument('id', type=int, required=True, help="The Note's id")

note_post_model = api.model('Note Post Model', {
    'title': fields.String(),
    'content': fields.String(),
    'user': fields.Nested(user_get_model)
})


note_delete_model = api.model('Note Delete Model', {
    'id': fields.Integer(required=True, description="The Note's id")
})
