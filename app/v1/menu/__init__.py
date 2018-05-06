# menu/__init__.py

from flask import Blueprint
from app.models.models import Menu

menu = Blueprint('menu', __name__)
menu_instance = Menu()

from . import views
