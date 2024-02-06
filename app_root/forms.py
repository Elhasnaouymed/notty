
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Regexp, EqualTo

from . import exceptions as excs


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[EqualTo('password')])
    submit = SubmitField('Register')

    def validate(self, extra_validators=None):
        if not FlaskForm.validate(self, extra_validators=extra_validators):
            return False

        from .models import DatabaseSimpleAPI
        dsi = DatabaseSimpleAPI()

        try:
            # > this should raise an error if the user is not found, which is false-positive in our case
            _ = dsi.get_user(self.username.data)
            return False
        except excs.UserNotFoundError:
            return True
