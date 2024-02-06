from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

from encryptman import CryptMan

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


def init_login_manager(app: Flask):
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'warning'
    login_manager.login_message = 'You must login first to access this page.'
    login_manager.needs_refresh_message = 'Login token changed, You must login again!'
    login_manager.needs_refresh_message_category = 'danger'

    @login_manager.user_loader
    def user_loader(user_token: int):
        from .models import UserModel
        return UserModel.query.filter_by(token=user_token).first()

    app.logger.debug('Done: login manager Initialized.')
