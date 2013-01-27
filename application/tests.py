"""
tests.py

Tests for jinja

"""

from application import app
from flask import request

@app.template_test()
def secure(url=None):
	if url == None:
		url = request.url
	return 'https://' == url[0:8] 