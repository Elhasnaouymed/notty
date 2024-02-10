import re
from datetime import datetime, UTC
from typing import *

from flask import current_app
from flask_login import UserMixin

from .extensions import db, cryptman
from . import exceptions as excs, StringNames
from .constants import Regex


class UserModel(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(256), unique=True, nullable=False)
    username = db.Column(db.String(32), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    join = db.Column(db.DateTime, default=datetime.now(UTC))

    def __init__(self, username: str, password: str):
        # > default values
        username = username.lower()
        # > validating inputs
        if self.user_exists(username):
            raise excs.UsernameAlreadyExistError(username)
        if cryptman.password_strength(password) < current_app.config.get(StringNames.REQUIRED_PASSWORD_STRENGTH):
            raise excs.WeakPasswordError()
        if not re.match(Regex.USERNAME_REGEX, username):
            raise excs.UsernamePatternError(username)
        # > setting instance variables
        self.username = username
        self.password = cryptman.generate_password_hash(password)
        self.token = cryptman.generate_user_token()

    def get_id(self):
        return self.token

    @classmethod
    def get_username_id(cls, username: str) -> Union[int, None]:
        user = cls.query.filter_by(username=username).first()
        return user.id if user else None

    @classmethod
    def user_exists(cls, username: str) -> bool:
        return cls.get_username_id(username) is not None


class NoteModel(db.Model):
    __tablename__ = 'note'
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(256))
    title = db.Column(db.String(128), nullable=False)
    content = db.Column(db.String(8192), nullable=False)
    create_date = db.Column(db.DateTime, default=datetime.now(UTC))
    last_modified = db.Column(db.DateTime, default=None)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('UserModel', backref=db.backref('notes', lazy='dynamic', cascade="all,delete"))

    def __init__(self, title: str, content: str, user: UserModel):
        if not re.match(Regex.NOTE_TITLE_REGEX, title):
            raise excs.NoteTitlePatternError(title)
        self.user = user
        self.token = cryptman.generate_note_unique_token()
        self.title = title
        self.content = content


# > TODO: probably this class needs its own module, I will do it soon
class DatabaseSimpleAPI:
    def __init__(self, autosave=False):
        self._autosave = autosave

    @staticmethod
    def _get_user_as_object(any_identifier: Union[UserModel, str, int]) -> UserModel:
        """ Makes sure the return is a User object, or Error """
        if isinstance(any_identifier, int):
            return UserModel.query.get(any_identifier)
        elif isinstance(any_identifier, str):
            return UserModel.query.filter_by(username=any_identifier).first()
        elif isinstance(any_identifier, UserModel):
            return any_identifier
        else:
            raise TypeError('Invalid argument type! User identifier must be int or str or User object.')

    @staticmethod
    def _get_note_as_object(any_identifier: Union[NoteModel, int, str]) -> NoteModel:
        """ Makes sure the return is a Note object, or Error """
        if isinstance(any_identifier, int):
            return NoteModel.query.get(any_identifier)
        elif isinstance(any_identifier, str):
            return NoteModel.query.filter_by(token=any_identifier).first()
        elif isinstance(any_identifier, NoteModel):
            return any_identifier
        else:
            raise TypeError('Invalid argument type! Note identifier must be int or Note object.')

    # ****************** User:

    def add_user(self, username: str, password: str, autosave=None):
        user = UserModel(username, password)
        db.session.add(user)
        if autosave or autosave is None and self._autosave:
            db.session.commit()
        return user

    def get_user(self, user: Union[str, int]):
        return self._get_user_as_object(user)

    def delete_user(self, user: Union[str, int, UserModel], autosave=None):
        obj_user = self._get_user_as_object(user)
        if not obj_user:
            raise excs.UserNotFoundError(user)
        db.session.delete(obj_user)
        #
        if autosave or autosave is None and self._autosave:
            db.session.commit()

    def check_user_login(self, user: Union[str, int], password: str):
        obj_user = self._get_user_as_object(user)
        if not obj_user:
            raise excs.UserNotFoundError(user)
        if not cryptman.check_password_hash(obj_user.password, password):
            raise excs.InCorrectPasswordError()
        return obj_user

    # ******************* Note:

    def add_note(self, title: str, content: str, user: Union[int, str, UserModel], autosave=None):
        user_obj = self._get_user_as_object(user)
        if not user_obj:
            raise excs.UserNotFoundError(user)
        #
        note = NoteModel(title, content, user_obj)
        db.session.add(note)
        if autosave or autosave is None and self._autosave:
            db.session.commit()
        return note

    def get_note(self, note: int | str):
        return self._get_note_as_object(note)

    def delete_note(self, note: Union[int, NoteModel], autosave=None):
        obj_note = self._get_note_as_object(note)
        if not obj_note:
            raise excs.NoteNotFoundError(note)
        db.session.delete(obj_note)
        if autosave or autosave is None and self._autosave:
            db.session.commit()

    def update_note(self, note: Union[int, NoteModel], title: str = None, content: str = None, autosave=None):
        obj_note = self._get_note_as_object(note)
        if not obj_note:
            raise excs.NoteNotFoundError(note)

        if title is not None:
            if not isinstance(title, str):
                raise TypeError('Note title must be str.')
            if not re.match(Regex.NOTE_TITLE_REGEX, title):
                raise excs.NoteTitlePatternError(title)
            obj_note.title = title

        if content is not None:
            if not isinstance(content, str):
                raise TypeError('Note content must be str.')
            obj_note.content = content
            obj_note.last_modified = datetime.now(UTC)

        if autosave or autosave is None and self._autosave:
            db.session.commit()

    # ***************** User Notes:

    def get_user_notes(self, user: Union[str, int, UserModel]):
        obj_user = self._get_user_as_object(user)
        if not obj_user:
            raise excs.UserNotFoundError(user)
        return obj_user.notes.all()
