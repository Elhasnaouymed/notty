from flask import Blueprint, render_template, redirect, url_for, flash, current_app

from ..extensions import db
from .. import exceptions as excs

auth = Blueprint('auth', __name__)


@auth.get('/login')
def login():
    return render_template('pages/login.html')


@auth.get('/signup')
def register():
    from ..forms import RegisterForm
    from ..models import UserModel, DatabaseSimpleAPI
    register_form = RegisterForm()

    if register_form.validate_on_submit():
        try:
            DatabaseSimpleAPI().add_user(register_form.username.data, register_form.password.data)
            current_app.logger.info(f'Done: New User Registered ({register_form.username.data}).')
        except excs.UsernamePatternError as ex:
            register_form.username.errors.append(str(ex))

    return render_template('pages/register.html', register_form=register_form)

