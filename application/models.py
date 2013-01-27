"""
models.py

App Engine datastore models

"""


from google.appengine.ext import ndb

class Product(ndb.Model):
	product_id = ndb.StringProperty(required=True)
	product_name = ndb.StringProperty()

class Branch(ndb.Model):
	# the channel id is either a root channel id e.g. 'stable' or a randomly generated alias id e.g. '9sd3jk'
	branch_id = ndb.StringProperty(required=True)
	branch_name = ndb.StringProperty()
	branch_description = ndb.StringProperty()
	product = ndb.KeyProperty(kind=Product)
	alias_for = ndb.KeyProperty(kind="Branch")
	is_core = ndb.BooleanProperty(default=False)
	is_alias = ndb.BooleanProperty(default=False)
	is_favourite = ndb.BooleanProperty(default=False)
	stable_build = ndb.KeyProperty(kind='Build') # left blank to get around circular reference problem
	beta_build = ndb.KeyProperty(kind='Build') # left blank to get around circular reference problem
	development_build = ndb.KeyProperty(kind='Build') # left blank to get around circular reference problem


class Build(ndb.Model):
	build_hash = ndb.StringProperty(required=True)
	uploaded_on = ndb.DateTimeProperty(auto_now_add=True)
	product = ndb.KeyProperty(kind=Product)
	product_version = ndb.StringProperty(required=True) # must be in format 6.5.12 (translates to: 000600050012)
	product_version_int = ndb.IntegerProperty(required=True)
	product_version_x = ndb.IntegerProperty(required=True) # used so you can get all builds within a major version
	product_version_y = ndb.IntegerProperty(required=True)
	product_version_z = ndb.IntegerProperty(required=True)
	branch = ndb.KeyProperty(kind=Branch)
	uploaded_by = ndb.StringProperty(default='Unspecified 0.0.0')
	is_stable = ndb.BooleanProperty(default=False)
	is_beta = ndb.BooleanProperty(default=False)
	is_development = ndb.BooleanProperty(default=True)