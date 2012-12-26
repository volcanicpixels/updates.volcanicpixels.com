"""
models.py

App Engine datastore models

"""


from google.appengine.ext import db

class Product(db.Model):
	product_id = db.StringProperty(required=True)
	product_name = db.StringProperty()

class Channel(db.Model):
	# the channel id is either a root channel id e.g. 'stable' or a randomly generated alias id e.g. '9sd3jk'
	channel_id = db.StringProperty(required=True)
	channel_name = db.StringProperty()
	channel_description = db.StringProperty()
	product = db.ReferenceProperty(reference_class=Product)
	alias_for = db.SelfReferenceProperty(collection_name='alias_channels')
	is_core = db.BooleanProperty(default=False,required=True)
	is_alias = db.BooleanProperty(default=False,required=True)
	is_favourite = db.BooleanProperty(default=False,required=True)
	active_build = db.ReferenceProperty() # left blank to get around circular reference problem


class Build(db.Model):
	build_hash = db.StringProperty(required=True)
	uploaded_on = db.DateTimeProperty(auto_now_add=True)
	product = db.ReferenceProperty(reference_class=Product)
	product_version = db.StringProperty(required=True) # must be in format 6.5.12 (translates to: 000600050012)
	product_version_int = db.IntegerProperty(required=True)
	product_version_x = db.IntegerProperty(required=True) # used so you can get all builds within a major version
	product_version_y = db.IntegerProperty(required=True)
	product_version_z = db.IntegerProperty(required=True)
	channel = db.ReferenceProperty(reference_class=Channel)
	uploaded_by = db.StringProperty(default='Unspecified 0.0.0')
	is_active = db.BooleanProperty(required=True,default=False)