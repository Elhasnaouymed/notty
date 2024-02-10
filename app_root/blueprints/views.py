from flask import Blueprint, render_template, redirect, url_for, flash, abort, current_app
from flask_login import current_user, login_required

from .. import exceptions as excs
from ..constants import *

views = Blueprint('views', __name__)


@views.get('/')
def home():
    return render_template('pages/index.html')


@views.get('/notes')
@login_required
def notes():
    from ..models import NoteModel
    # > get all notes ordered by last modified and created date (simple, we can do more but things will get complicated)
    user_notes = current_user.notes.order_by(NoteModel.last_modified.desc(), NoteModel.create_date.desc()).all()
    oldest_note = user_notes[-1] if user_notes else None  # get the oldest note of current user if there are any
    return render_template('pages/notes.html', notes=user_notes, oldest_note=oldest_note)


@views.route('/create_note', methods=['GET', 'POST'])
@login_required
def create_note():
    from ..forms import NoteForm
    from ..models import DatabaseSimpleAPI
    note_form = NoteForm()

    if note_form.validate_on_submit():
        dsi = DatabaseSimpleAPI()
        try:
            # > try to add the note directly
            note = dsi.add_note(note_form.title.data, note_form.content.data, current_user, True)
        except excs.NottyException as ex:  # when any error happen within the known app errors
            flash(str(ex), 'danger')  # flash the error message
        else:
            # when success
            flash('Your Note was created successfully', 'success')
            current_app.logger.info(f'Done: Note #{note.id} created by @{current_user.username}')  # log for debugging
            return redirect(url_for('views.notes'))

    return render_template('pages/create_note.html', note_form=note_form)


@views.get('/note/<string:token>')
@login_required
def view_note(token: str):
    from ..models import DatabaseSimpleAPI
    note = DatabaseSimpleAPI().get_note(token)  # get note by its token
    if not note:
        return abort(SCodes.NOT_FOUND_404)  # when no note was found, 404

    # > check if the note owner is the same as logged in
    if note.user != current_user:
        flash('You do not have the privileges to view this Note!', 'danger')
        current_app.logger.warning(f'WARNING: user @{current_user.username} tried to access other\'s note #{note.id}')  # log for debugging
        return redirect(url_for('views.notes'))
    return render_template('pages/view_note.html', note=note)


@views.get('/about')
def about():
    return render_template('pages/about.html')

