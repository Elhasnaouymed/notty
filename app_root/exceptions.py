"""
    Having an exception for each possible error might become handy, like:

    you want to return the exact error message of what happen to the user, instead of checking each error in the code with `if` statements,
    you can raise the Python exception
"""

from .constants import Regex
from typing import *


class NottyException(Exception):
    message = 'Notty Error'

    def __str__(self):
        return self.message


# Database Models

class UserException(NottyException): pass
class NoteException(NottyException): pass


# Error Types

class PatternException(NottyException): pass
class SingularityException(NottyException): pass
class NullException(NottyException): pass

#


class UsernamePatternError(UserException, PatternException):
    def __init__(self, username: str) -> None:
        self.message = f"Username '{username}' doesn't respect regex('{Regex.USERNAME_REGEX}')"


class UsernameAlreadyExistError(UserException, SingularityException):
    def __init__(self, username: str) -> None:
        self.message = f"Username '{username}' already exists."


class UserNotFoundError(UserException, NullException):
    def __init__(self, user: Union[str, int]) -> None:
        attribute = 'id' if isinstance(user, int) else 'username'
        self.message = f"No such User with {attribute} == {user}"


class WeakPasswordError(UserException, PatternException):
    def __init__(self):
        self.message = "You chosen a weak password, Please choose a better one."


class NoteTitlePatternError(NoteException, PatternException):
    def __init__(self, title: str) -> None:
        self.message = f"Note Title {title} doesn't respect regex('{Regex.NOTE_TITLE_REGEX}')"


class NoteNotFoundError(NoteException, NullException):
    def __init__(self, note_id: int) -> None:
        self.message = f"No such Note with id == {note_id}"
