# menu/__init__.py

from flask import Blueprint

menu = Blueprint('menu',__name__)

from . import views
