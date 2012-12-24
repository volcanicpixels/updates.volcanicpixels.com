"""
filters.py

Filters for jinja

"""

from application import app

@app.template_filter('slugify')
def slugify_filter(s):
	return s.replace(' ','-').lower()