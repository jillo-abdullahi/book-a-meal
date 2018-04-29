"""menu/views.py"""
from flask import request, jsonify

from . import menu, menu_instance


@menu.route('/menu', methods=['GET'])
def get_meals_menu():
    """Test getting of current menu"""
    if not menu_instance.menu:
        return jsonify({"message": "menu not set"}), 204
    return jsonify({"Meals Menu": menu_instance.menu}), 200


@menu.route('/menu', methods=['POST'])
def set_menu():
    """Test setting of menu"""
    get_menu = request.get_json()

    menu_instance.create_menu(get_menu)

    return jsonify({"Menu": menu_instance.menu}), 201
