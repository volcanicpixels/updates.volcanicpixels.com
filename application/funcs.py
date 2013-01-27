import yaml
import os
import string
import random

def load_data(file_name):
	data = open(os.path.join(os.path.dirname(__file__),'data',file_name)).read()
	return yaml.load(data)

def random_key(length=6,chars=string.ascii_lowercase + string.digits):
	return ''.join(random.choice(chars) for x in range(length))


"""
Primarily used for serializing datastore models
"""

def make_json_safe(model):
	output = {}

	for key, prop in model.properties().iteritems():
		value = getattr(model, key)

		if value is None or isinstance(value, SIMPLE_TYPES):
			output[key] = value
		elif isinstance(value, datetime.date):
			# Convert date/datetime to ms-since-epoch ("new Date()").
			ms = time.mktime(value.utctimetuple())
			ms += getattr(value, 'microseconds', 0) / 1000
			output[key] = int(ms)
		elif isinstance(value, db.GeoPt):
			output[key] = {'lat': value.lat, 'lon': value.lon}
		elif isinstance(value, db.Model):
			output[key] = to_dict(value)
		else:
			raise ValueError('cannot encode ' + repr(prop))

	return output