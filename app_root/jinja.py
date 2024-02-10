"""
    In this module, we should define jinja filters and any code that is specifically used in Jinja-Html templates
    also contains a method that will integrate that with our Jinja env (def init_jinja_env)
"""

from flask import Flask
from flask_login import current_user

from .extensions import cryptman
from .constants import *


def logout_token():
    """ generates a logout token for current user and returns it (returns None when no user logged-in) """
    if current_user.is_authenticated:
        return cryptman.serial_crypt(current_user.username, StringNames.LOGOUT_TOKEN_NAME)


def init_jinja_env(app: Flask):
    """ this method adds jinja filters and context variables into the jinja env """
    app.jinja_env.globals['logout_token'] = logout_token
    app.jinja_env.globals['DTFORMATS'] = DTFormats
