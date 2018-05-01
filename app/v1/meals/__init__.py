# v1/meals/__init__.py

from flask import Blueprint

from app.models.models import Meals

meals = Blueprint('meals', __name__)
meal_instance = Meals()

from . import views
