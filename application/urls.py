"""
urls.py

URL dispatch route mappings and error handlers

"""

from flask import render_template, flash
from google.appengine.api import memcache
from application import app
from decorators import login_required, admin_required, cached


## URL dispatch rules

# Say hello
#app.add_url_rule('/hello/<username>', 'say_hello', view_func=views.say_hello)

# Examples list page
#app.add_url_rule('/examples', 'list_examples', view_func=views.list_examples, methods=['GET', 'POST'])

# Delete an example (post method only)
#app.add_url_rule('/examples/delete/<int:example_id>', view_func=views.delete_example, methods=['POST'])


## Error handlers
# Handle 404 errors
@cached
@app.errorhandler(404)
def page_not_found(e):
	return render_template('not_found.html'), 404

# Handle 500 errors
@app.errorhandler(500)
def server_error(e):
	return render_template('internal_error.html'), 500


# App Engine warm up handler
# See http://code.google.com/appengine/docs/python/config/appconfig.html#Warming_Requests
@app.route('/_ah/warmup')
def warmup():
	"""App Engine warmup handler
	See http://code.google.com/appengine/docs/python/config/appconfig.html#Warming_Requests

	"""
	return ''


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
	memcache_stats = memcache.get_stats()
	return render_template('cache.html',memcache_stats=memcache_stats)