from flask import Blueprint, render_template, redirect, url_for, flash

auth = Blueprint('auth', __name__)


@auth.get('/login')
def login():
    return 'Login :)'


@auth.get('/signup')
def register():
    return 'Register :)'

