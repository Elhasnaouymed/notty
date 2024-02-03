import os
import logging

from flask import Flask

from .constants import *
from .extensions import *
from .jinja import init_jinja_env
from .cli import init_cli
from .api import init_api
from .config import DevConfig
from .blueprints import init_blueprints
from .models import UserModel, NoteModel


def init_logger(app: Flask, overwrite=True):
    """
    sets the app logger to print to screen and also save to file
    :param overwrite: whether to overwrite if log file exists or append to it
    :param app: the target Flask app
    :return: None
    """
    # create log directory
    try:
        os.makedirs(os.path.dirname(LOG_FILE))
    except Exception:
        pass

    if overwrite:
        try:
            os.remove(LOG_FILE)
        except FileNotFoundError:
            pass

    # app.logger = logging.Logger(__name__)
    # < instead of overriding a property, > change the existing logger configuration
    app.logger.setLevel(logging.DEBUG)  # set logger level
    #
    file_handler = logging.FileHandler(LOG_FILE)  # set a file to log to
    formatter = logging.Formatter(LOGGER_FILE_FORMATTER)
    file_handler.setFormatter(formatter)
    #
    steam_handler = logging.StreamHandler()  # set the steam handler to print out
    formatter = logging.Formatter(LOGGER_STREAM_FORMATTER)
    steam_handler.setFormatter(formatter)
    #
    app.logger.addHandler(file_handler)
    app.logger.addHandler(steam_handler)


def configure(app: Flask):
    app.config.from_object(DevConfig)
    app.logger.debug('Done: App Configured.')


def create_app():
    app = Flask(__name__)
    # > configuration
    init_logger(app, True)
    configure(app)

    # > blueprints and api
    init_api(app)
    init_blueprints(app)

    # > anything that utilizes database
    init_db(app)
    init_migrate(app)

    # > environments (jinja, shell)
    init_jinja_env(app)
    init_cli(app)

    # login_manager
    init_login_manager(app)

    return app
