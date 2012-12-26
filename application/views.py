"""
views.py

URL route handlers

"""

from google.appengine.api import users, memcache
from google.appengine.runtime.apiproxy_errors import CapabilityDisabledError

from flask import render_template, flash, url_for, redirect
from decorators import login_required, admin_required, cached

from application import app
from funcs import load_data



"""
Public views
"""


@app.route( '/' )
@cached
def home():
	return render_template('home.html')

@app.route( '/api-docs/')
@cached
def api_docs():
	api = load_data('api.yaml')
	return render_template('api_docs.html',api=api)



"""
Admin views
"""


@app.route( '/api-keys/')
@admin_required
@cached
def api_keys():
	api_keys = load_data('api_keys.yaml')
	return render_template('api_keys.html',api_keys=api_keys)
	
# Flushes the page cache
@app.route('/cache/')
@app.route('/cache/<method>')
@admin_required
def cache(method=None):
	if method == 'flush':
		if memcache.flush_all():
			flash('Cache successfully flushed.', 'success')
		else:
			flash('Cache could not be flushed.', 'error')
		return redirect(url_for('cache'))
	memcache_stats = memcache.get_stats()
	return render_template('cache.html',memcache_stats=memcache_stats)

"""
Error views
"""

@cached
@app.errorhandler(404)
def page_not_found(e):
	return render_template('/errors/not_found.html'), 404

# Handle 500 errors
@app.errorhandler(500)
def server_error(e):
	return render_template('/errors/internal_error.html'), 500


# Handle 405 errors
@cached
@app.errorhandler(405)
def server_error(e):
	return render_template('/errors/method_not_allowed.html'), 500


"""
System views
"""

# App Engine warm up handler
# See http://code.google.com/appengine/docs/python/config/appconfig.html#Warming_Requests
@app.route('/_ah/warmup')
def warmup():
	"""App Engine warmup handler
	See http://code.google.com/appengine/docs/python/config/appconfig.html#Warming_Requests

	"""
	return ''