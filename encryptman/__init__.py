"""
    TODO: make the cryptman check if its initialized before doing local methods
"""

__version__ = '0.1'
__license__ = 'GPL v2'
__author__ = 'codeberg.org/elhasnaouymed'


from itsdangerous import URLSafeSerializer, TimestampSigner
from werkzeug.security import generate_password_hash, check_password_hash
from secrets import token_hex
from hashlib import sha256
from password_strength import PasswordStats
from flask import Flask


class CryptMan:
    def __init__(self, app: Flask = None):
        """
        This class generates the necessary hashes and tokens for use in the project
        :param secret_key: an optional secret key, it will be hashed so
        """
        self._app = app
        self._secret_key = None
        self._initialized = False
        if app:
            self.init_app(app)

    def init_app(self, app: Flask):
        # > if secret_key argument is None, it defaults to the app's SECRET_KEY, or into the sha256 hash of the app's name
        secret_key = sha256(app.name.encode()).hexdigest() if not app.secret_key else app.secret_key
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

    @staticmethod
    def generate_note_unique_token():
        return f'nut:{token_hex(16)}'
        # < nut stands for Note Unique Token

    @classmethod
    def password_strength(cls, password: str):
        """ returns the password strength as float(0..1) """
        return PasswordStats(password).strength()

    def serial_crypt(self, salt: str, text: str):
        uss = URLSafeSerializer(self._secret_key, salt)
        ts = TimestampSigner(self._secret_key, salt)
        serial = uss.dumps(text)
        stamped = ts.sign(serial)
        return stamped.decode()

    def serial_decrypt(self, salt: str, serial: str, max_age: int):
        uss = URLSafeSerializer(self._secret_key, salt)
        ts = TimestampSigner(self._secret_key, salt)

        unsigned = ts.unsign(serial, max_age=max_age)  # raises SignatureExpired or BadTimeSignature
        original = uss.loads(unsigned)

        return original
