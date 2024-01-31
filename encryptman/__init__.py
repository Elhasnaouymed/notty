__version__ = '0.1'
__license__ = 'GPL v2'
__author__ = 'codeberg.org/elhasnaouymed'

from flask import current_app
from itsdangerous import URLSafeSerializer, TimestampSigner
from werkzeug.security import generate_password_hash, check_password_hash
from secrets import token_hex, token_bytes, token_urlsafe
from hashlib import sha256
from password_strength import PasswordStats


class CryptMan:
    def __init__(self, secret_key: str = None):
        """
        This class generates the necessary hashes and tokens for use in the project
        :param secret_key: an optional secret key, it will be hashed so
        """
        self._secret_key = None
        self._initialized = False
        if secret_key is not None:
            self.init_app(secret_key)

    def init_app(self, secret_key: str = None):
        """
        :param secret_key: Optional; (over-write s the initialized secret key if there was one)
        """
        # > if secret_key argument is None, it defaults to the app's SECRET_KEY, or into the sha256 hash of the app's name
        secret_key = current_app.config.get('SECRET_KEY', sha256(current_app.name.encode()).hexdigest()) if not secret_key else secret_key
        # > secret_key get hashed for security reasons (not a big deal)
        self._secret_key = sha256(secret_key.encode()).hexdigest()
        self._initialized = True

    @staticmethod
    def generate_password_hash(password: str):
        return generate_password_hash(password)

    @staticmethod
    def check_password_hash(hash_: str, password: str):
        return check_password_hash(hash_, password)

    @staticmethod
    def generate_user_token():
        """
        get a random User Login Token to use instead of user ID
        https://flask-login.readthedocs.io/en/latest/#alternative-tokens
        """
        return f'ult:{token_hex(16)}'
        # < ult stands for User Login Token

    @classmethod
    def password_strength(cls, password: str):
        """ returns the password strength as float(0..1) """
        return PasswordStats(password).strength()
