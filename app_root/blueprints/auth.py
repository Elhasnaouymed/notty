from flask import Blueprint, render_template, redirect, url_for, flash

auth = Blueprint('auth', __name__)


@auth.get('/login')
def login():
    return render_template('pages/login.html')


@auth.get('/signup')
def register():
    return render_template('pages/register.html')

