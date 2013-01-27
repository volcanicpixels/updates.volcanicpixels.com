"""
filters.py

Filters for jinja

"""

from application import app

@app.template_filter('slugify')
def slugify(s):
	return s.replace(' ','-').lower()