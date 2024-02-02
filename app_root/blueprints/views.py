from flask import Blueprint, render_template, redirect, url_for, flash

views = Blueprint('views', __name__)


@views.get('/')
def home():
    return render_template('pages/index.html')


@views.get('/notes')
def notes():
    return render_template('pages/notes.html')


@views.get('/about')
def about():
    return render_template('pages/about.html')

