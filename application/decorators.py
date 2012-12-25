"""
decorators.py

Decorators for URL handlers

"""

from functools import wraps
from google.appengine.api import users, memcache
from flask import make_response, redirect, request, abort
from settings import CACHE_TIMEOUT, CACHE_ENABLED


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
		pass
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