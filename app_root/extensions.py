from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from encryptman import CryptMan


db = SQLAlchemy()
migrate = Migrate()
cryptman = CryptMan()
