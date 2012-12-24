import yaml
import os

def load_data(file_name):
	data = open(os.path.join(os.path.dirname(__file__),'data',file_name)).read()
	return yaml.load(data)