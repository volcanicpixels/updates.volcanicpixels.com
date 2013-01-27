"""
Initialize Flask API Blueprint

"""

from flask import Blueprint

app = Blueprint('api', __name__)
api_id = 'updates.volcanicpixels.com'

import views
