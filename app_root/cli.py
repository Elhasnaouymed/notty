"""
    This module will contain the CLI interface commands and context processor, Just to make things modular and readable,
    it is not important in small apps, but its good practice (in my opp)
    will also contain a method to initialize that with Flask app (def init_cli)
"""

from flask import Flask
from flask.cli import AppGroup

from .extensions import db


def _create_default_records(app: Flask):
    from .models import DatabaseSimpleAPI
    dsi = DatabaseSimpleAPI()
    try:
        dsi.add_user('admin', 'admin', autosave=True)
        app.logger.info('Done: Default user admin:admin Created.')
    except Exception as ex:
        app.logger.warning('Warning: Default user admin already exists.')


def _register_shell_commands(app: Flask):
    datab = AppGroup('database')

    @datab.command()
    def create():
        db.create_all()
        _create_default_records(app)

    app.cli.add_command(datab)


def _register_shell_context(app: Flask):
    from .models import UserModel, NoteModel, DatabaseSimpleAPI

    @app.shell_context_processor
    def context():
        return {
            'User': UserModel,
            'Note': NoteModel,
            'DbApi': DatabaseSimpleAPI
        }


def init_cli(app: Flask):
    _register_shell_commands(app)
    _register_shell_context(app)
