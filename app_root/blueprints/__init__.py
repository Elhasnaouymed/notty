from flask import Flask

from .views import views
from .auth import auth


def init_blueprints(app: Flask):
    app.register_blueprint(views)
    app.register_blueprint(auth)
    app.logger.debug('Done: Blueprints registered (views, auth).')
    
