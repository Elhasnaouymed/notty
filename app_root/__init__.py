import os
import logging

from flask import Flask

from .constants import *
from .extensions import db, cryptman, migrate


def init_logger(app: Flask, overwrite=True):
    """
    sets the app logger to print to screen and also save to file
    :param overwrite:
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
    # < except of overriding a property, > override the logger config
    app.logger.setLevel(logging.DEBUG)  # set logger level
    #
    file_handler = logging.FileHandler(LOG_FILE)  # set a file to log to
    formatter = logging.Formatter(LOGGER_FILE_FORMATTER)
    file_handler.setFormatter(formatter)
    #
    steam_handler = logging.StreamHandler()  # set the steam handler to print out
    formatter = logging.Formatter(LOGGER_STEAM_FORMATTER)
    steam_handler.setFormatter(formatter)
    #
    app.logger.addHandler(file_handler)
    app.logger.addHandler(steam_handler)


def configure(app: Flask):
    from .config import DevConfig
    app.config.from_object(DevConfig)
    app.logger.debug('Done: App Configured.')


def init_db(app: Flask):
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.logger.debug('Done: Database Initialized.')


def create_app():
    app = Flask(__name__)
    init_logger(app, True)
    configure(app)
    init_db(app)

    from .api import init_api
    init_api(app)
    app.logger.debug('Done: Rest API initialized.')

    from .jinja import init_jinja_env
    init_jinja_env(app)

    return app
