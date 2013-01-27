"""
views.py

URL route handlers

"""

from . import app, api_id
from application.decorators import cached, json_response, api_key_required, post_request
from flask import make_response, redirect, url_for, request
from flask.views import View

from application.models import Product
from application.funcs import random_key
from google.appengine.datastore.datastore_query import Cursor

import logging

"""
API methods
"""

@app.route('/products/',methods=['GET'])
@json_response
def list_products(start_token=''):
	items_per_page = 100
	cursor = Cursor(urlsafe=start_token)
	products, next_cursor, more = Product.query().order(Product.product_id).fetch_page(items_per_page,start_cursor=cursor)

	items = []
	for product in products:
		items.append({
			'product_id': product.product_id,
			'product_name': product.product_name
		})

	response = {
		'kind': api_id + '#productList',
		'totalItems': len(products),
		'itemsPerPage': items_per_page,
		'items': items
	}

	if more and next_cursor:
		response['nextPageToken'] = next_cursor
	return response


@app.route('/products/',methods=['POST'])
@api_key_required
@json_response
@post_request
def create_product(product_id=None,product_name=None):
	if product_id is None or len(product_id) <= 3:
		product_id = random_key(10)

	existing_products = Product.query(Product.product_id == product_id).fetch(1)

	if len(existing_products) != 0:
		import logging
		logging.error('Product with ID "' + product_id + '" already exists.' )
		return make_error(400,'A product with ID ' + product_id + ' already exists, overwriting is forbidden.')

	product = Product(product_id=product_id)
	if product_name is not None:
		product.product_name = product_name
	product.put()
	return product.product_id

@app.route('/products/<product_id>/',methods=['DELETE'])
@api_key_required
@json_response
def delete_product(product_id):
	product = Product.query(Product.product_id == product_id).get()
	if product is None:
		return make_error(404,"This product does not exist, so can't be deleted.")
	product.key.delete()
	return {
		'success': "Product deleted successfully."
	}


def make_error(error_code=500, error_message="No error message specified", errors=[]):
	return {
		'error': {
			'code': error_code,
			'message': error_message,
			'errors': errors
		}
	}



"""
Redirects
"""


@app.route( '/' )
@cached
def api():
	return redirect(url_for('api_docs'))