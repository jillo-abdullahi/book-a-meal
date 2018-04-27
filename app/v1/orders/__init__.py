"""orders/__init__.py"""
from flask import Blueprint
from app.models.models import Orders

orders = Blueprint('orders',__name__)
orders_instance = Orders()

from . import views
