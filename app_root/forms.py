"""
    The forms are defined here
"""


from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Regexp, EqualTo

from .constants import Regex


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[EqualTo('password')])
    agreement = BooleanField('Agree to live Libre and Free as in Freedom.', validators=[DataRequired()])
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class NoteForm(FlaskForm):
    title = StringField('Title', validators=[Regexp(Regex.NOTE_TITLE_REGEX, message=f'Title must respect RegEx({Regex.NOTE_TITLE_REGEX})')])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Create Note')
