from flask.config import Config


class DevConfig(Config):
    SECRET_KEY = '5614047081e08f130138f456b54cdfb0621137ae550165507b9e17cbb1ee4b20'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///dev.db'

    PASSWORD_STRENGTH = 0
