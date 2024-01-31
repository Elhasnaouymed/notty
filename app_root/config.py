from flask.config import Config


class DevConfig(Config):
    # > extension configs
    SECRET_KEY = '5614047081e08f130138f456b54cdfb0621137ae550165507b9e17cbb1ee4b20'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///dev.db'

    # > these are the custom configs for this app
    # > if you change the names of them, make sure you change it also on constants.Strings module
    REQUIRED_PASSWORD_STRENGTH = .0  # must be a float between 0..1
