from flask import Flask


def init_jinja_env(app: Flask):
    from .models import UserModel, NoteModel, DatabaseSimpleAPI

    @app.shell_context_processor
    def context():
        return {
            'User': UserModel,
            'Note': NoteModel,
            'DbApi': DatabaseSimpleAPI
        }
