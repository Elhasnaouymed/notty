from itsdangerous.exc import SignatureExpired, BadTimeSignature, BadSignature

from flask import Blueprint, render_template, redirect, url_for, flash, current_app
from flask_login import login_user, logout_user, login_required, current_user

from ..extensions import db, cryptman
from ..constants import *
from .. import exceptions as excs

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    # > when user is already logged in, don't allow him to login again !
    if current_user.is_authenticated:
        flash('You are already logged in.', 'secondary')
        return redirect(url_for('views.home'))

    from ..forms import LoginForm
    from ..models import DatabaseSimpleAPI
    login_form = LoginForm()

    if login_form.validate_on_submit():
        try:
            # > try fetching the user, if anything wrong, error will be raised
            user = DatabaseSimpleAPI().check_user_login(login_form.username.data, login_form.password.data)
        except excs.UserNotFoundError as ex:  # the ex.message contains the error message and u can get it with str(ex)
            login_form.username.errors.append(str(ex))
        except excs.InCorrectPasswordError as ex:
            login_form.password.errors.append(str(ex))
        else:
            # > when the user was fetched with no error
            login_user(user, login_form.remember.data)  # login it with his choice to remember or not
            flash(f'Welcome back {user.username}', 'success')  # welcome him on the web page
            current_app.logger.info(f'Done: User @{user.username} logged in.')  # log for debugging
            return redirect(url_for('views.notes'))  # go to notes page

    return render_template('pages/login.html', login_form=login_form)


@auth.route('/signup', methods=['GET', 'POST'])
def register():
    # > when user is already logged in, don't allow him to login again !
    if current_user.is_authenticated:
        flash('You can not register while logged in.', 'secondary')
        return redirect(url_for('views.home'))

    from ..forms import RegisterForm
    from ..models import DatabaseSimpleAPI
    register_form = RegisterForm()

    if register_form.validate_on_submit():
        try:
            # > try to create new user and saving it into database automatically, if anything goes wrong, error will be raised
            user = DatabaseSimpleAPI().add_user(register_form.username.data, register_form.password.data, autosave=True)
            # < if the execution reached here, that means the used creation succeeded
            current_app.logger.info(f'Done: New User Registered ({register_form.username.data}).')  # log for debugging
        # > I take the exceptions separately just to know where to put the error message (username field or password field) to get shown on the web page later
        except (excs.UsernameAlreadyExistError, excs.UsernamePatternError) as ex:
            register_form.username.errors.append(str(ex))
        except excs.WeakPasswordError as ex:
            register_form.password.errors.append(str(ex))
        else:
            # > flash a success message and go to log-in,
            # > this code can be put up inside the try statement, no difference ¯\_(ツ)_/¯
            flash('You Registered Successfully, Please login.', 'success')
            return redirect(url_for('auth.login'))

    return render_template('pages/register.html', register_form=register_form)


@auth.route('/logout/<string:token>')
@login_required
def logout(token: str):
    """ logout the user after checking the logout token """
    try:
        # > get expiration date for the token (in seconds)
        token_max_age = current_app.config.get(StringNames.LOGOUT_TOKEN_EXPIRE_SECONDS, 3600)
        # > next line deserializes the token with checking its timestamp using app config LOGOUT_TOKEN_EXPIRE_SECONDS
        plaintext = cryptman.serial_decrypt(current_user.username, token, token_max_age)
    except SignatureExpired as ex:
        # | when timestamp is invalid
        flash('Your Logout token is expired, Please try again.', 'warning')
        return redirect(url_for('views.home'))
    except (BadSignature, BadTimeSignature) as ex:
        # | when token is broken, or it's not even a token
        flash('Your try to Logout failed, Please try again.', 'warning')
        return redirect(url_for('views.home'))

    # - so far, token is valid, next lets check if it's a logout token or something else

    if plaintext != StringNames.LOGOUT_TOKEN_NAME:
        # | when token is valid but not for logging out :/
        current_app.logger.warning(f'WARNING: logout endpoint received a valid text("{plaintext}") as token !')  # log for future debugging
        flash('Your try to Logout failed badly, Please try again.', 'error')
        return redirect(url_for('views.home'))

    # > now, we've checked everything, lets logout :)
    logout_user()
    return redirect(url_for('auth.login'))
