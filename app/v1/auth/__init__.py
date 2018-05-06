"""v1/auth/__init__.py"""
from flask import Blueprint

# Local import
from app.models.models import User


auth = Blueprint('auth', __name__)
user_instance = User()

from . import views
