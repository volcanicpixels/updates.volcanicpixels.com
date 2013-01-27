"""
Initialize Flask Admin Blueprint

"""

from flask import Blueprint

app = Blueprint('admin', __name__)

import views
