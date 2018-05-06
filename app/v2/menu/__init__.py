# menuV2/__init__.py

from flask import Blueprint

menu = Blueprint('menu', __name__)  # Version 1
menuV2 = Blueprint('menuV2', __name__)  # Version 2

from . import views
