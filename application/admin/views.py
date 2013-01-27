"""
views.py

URL route handlers

"""

from . import app
from application.decorators import cached
from flask import make_response, redirect, url_for, request
from flask.views import View


@app.route('/')
def admin():
	return 'bob'