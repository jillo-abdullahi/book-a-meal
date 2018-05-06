# V2/orders/__init__.py

from flask import Blueprint

orders = Blueprint('orders', __name__)  # Version 1
ordersV2 = Blueprint('ordersV2', __name__)  # Version 2

from . import views
