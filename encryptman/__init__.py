__version__ = '0.1'
__license__ = 'GPL v2'
__author__ = 'codeberg.org/elhasnaouymed'

from itsdangerous import URLSafeSerializer, TimestampSigner
from werkzeug.security import generate_password_hash, check_password_hash
from secrets import token_hex, token_bytes, token_urlsafe
from hashlib import sha256
from password_strength import PasswordStats


class CryptMan:
    def __init__(self, secret_key: str = None):
        """
        This class generates the necessary hashes and tokens for use in the project
        :param secret_key: optional application secret key that will be hashed anyway :)
        """
        self._secret_key = None
        self._initialized = False
        if secret_key is not None:
            self.init_app(secret_key)

    def init_app(self, secret_key: str = None):
        """
        :param secret_key: overwrites the initialized secret key if there was one
        """
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
        return f'ult:{token_hex(16)}'

    @classmethod
    def password_strength(cls, password: str):
        return PasswordStats(password).strength()
