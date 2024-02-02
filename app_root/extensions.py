from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from encryptman import CryptMan
from flask_login import LoginManager


db = SQLAlchemy()
migrate = Migrate()
cryptman = CryptMan()
login_manager = LoginManager()


def init_db(app: Flask):
    from . import models
    db.init_app(app)
    app.logger.debug('Done: Database Initialized.')


def init_migrate(app: Flask):
    migrate.init_app(app, db)
    app.logger.debug('Done: Migrate Initialized.')
