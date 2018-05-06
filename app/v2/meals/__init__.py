# v1/meals/__init__.py

from flask import Blueprint

meals = Blueprint('meals', __name__)  # Version 1
mealsV2 = Blueprint('mealsV2', __name__)  # Version 2

from . import views
