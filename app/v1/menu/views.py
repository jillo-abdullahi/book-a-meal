# menu/views.py

from flask_api import FlaskAPI
from flask import request, jsonify
from . import menu

meals_menu = []

@menu.route('/menu', methods=['GET'])
def get_meals_menu():

	return jsonify({"Meals Menu": meals_menu}),200

