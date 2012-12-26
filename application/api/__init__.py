"""
Initialize Flask API Blueprint

"""

from flask import Blueprint

app = Blueprint('api', __name__)


import views
