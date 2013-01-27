"""
decorators.py

Decorators for URL handlers

"""

from functools import wraps
from google.appengine.api import users, memcache
from flask import make_response, redirect, request, abort, jsonify
from settings import CACHE_TIMEOUT, CACHE_ENABLED
import json
import logging


def login_required(func):
	"""Requires standard login credentials"""
	@wraps(func)
	def decorated_view(*args, **kwargs):
		if not users.get_current_user():
			return redirect(users.create_login_url(request.url))
		return func(*args, **kwargs)
	return decorated_view


def admin_required(func):
	"""Requires App Engine admin credentials"""
	@wraps(func)
	def decorated_view(*args, **kwargs):
		if users.get_current_user():
			if not users.is_current_user_admin():
				abort(401)  # Unauthorized
			return func(*args, **kwargs)
		return redirect(users.create_login_url(request.url))
	return decorated_view


def api_key_required(func):
	"""Requires Volcanic Pixels API key"""
	@wraps(func)
	def decorated_view(*args, **kwargs):
		return func(*args,**kwargs)
	return decorated_view

def cached(func,timeout=None):
	"""Caches response"""
	if timeout is None:
		timeout = CACHE_TIMEOUT
	@wraps(func)
	def decorated_view(*args, **kwargs):
		if not CACHE_ENABLED:
			return func(*args, **kwargs)
		else:
			response = memcache.get(request.path,namespace='response_cache')
			if response is None:
				response = make_response(func(*args, **kwargs))
				memcache.add(request.path, response, timeout,namespace='response_cache')
				response.headers.add('Added-To-Cache',request.path)
			else:
				response.headers.add('From-Cache',request.path)
			return response
	return decorated_view


def json_response(func):
	"""Makes the response a json string"""
	@wraps(func)
	def decorated_view(*args, **kwargs):
		data = func(*args, **kwargs)
		data = json.dumps(data)
		response = make_response(data)
		response.headers['Content-Type'] = 'application/json'
		return response
	return decorated_view


def post_request(func):
	@wraps(func)
	def decorated_view(*args,**kwargs):
		kwargs = {}
		for post_variable in request.form:
			kwargs[post_variable] = request.form[post_variable]
		return func(*args,**kwargs)
	return decorated_view

def serialize_object( data ):
	"""
		Serializes an object to one of the following types:
		 - list
		 - dict
		 - string
		 - integer
	"""
	logging.info('Serializing')
	if data is str:
		return data
	if data is int:
		return data

	if data is dict:
		for key in data:
			data[key] = serialize_object( data[key] )
		return data

	if data is list:
		return_object = []
		for child_data in data:
			return_object.append( serialize_object(child_data) )
		return return_object

	if data is object:
		logging.info('Object encountered')
		if 'serialize_object' in dir(data):
			return data.serialize_object()
		else:
			logging.error(dir(data))
	else:
		logging.error( type(data) )
		logging.error( data )


