"""
views.py

URL route handlers

Note that any handler params must match the URL route params.
For example the *say_hello* handler, handling the URL route '/hello/<username>',
  must be passed *username* as the argument.

"""

from google.appengine.api import users
from google.appengine.runtime.apiproxy_errors import CapabilityDisabledError

from flask import render_template, flash, url_for, redirect
from decorators import login_required, admin_required, cached

from application import app
from funcs import load_data


@app.route( '/' )
@cached
def home():
	return render_template('home.html')

@app.route( '/api-docs/')
@cached
def api_docs():
	api = load_data('api.yaml')
	return render_template('api_docs.html',api=api)


@app.route( '/api-keys/')
@admin_required
@cached
def api_keys():
	api_keys = load_data('api_keys.yaml')
	return render_template('api_keys.html',api_keys=api_keys)

@app.route( '/api/' )
@cached
def api():
	return redirect(url_for('api_docs'))

