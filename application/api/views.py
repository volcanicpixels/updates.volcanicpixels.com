"""
views.py

URL route handlers

"""

from application.api import app
from application.decorators import cached, json_response, api_key_required
from flask import make_response, redirect, url_for
from flask.views import View

from application.models import Product




"""
API methods
"""

@app.route('/products/',methods=['GET'])
@json_response
def list_products():
	products = Product.all().get()
	return products


@app.route('/products/',methods=['POST'])
@api_key_required
@json_response
def create_product():
	return {}




"""
Redirects
"""


@app.route( '/' )
@cached
def api():
	return redirect(url_for('api_docs'))