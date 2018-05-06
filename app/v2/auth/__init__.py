"""v1/auth/__init__.py"""
from flask import Blueprint

auth = Blueprint('auth', __name__)  # Version 1
authV2 = Blueprint('authV2', __name__)  # Version 2

from . import views
