"""menu/views.py"""
from flask import request, jsonify
from flask_jwt_extended import jwt_required

from . import menu, menu_instance
from app.utilities import check_admin


@menu.route('/menu', methods=['GET'])
@jwt_required
def get_meals_menu():
    """Test getting of current menu"""
    if not menu_instance.menu:
        return jsonify({"message": "menu not set yet"}), 404
    return jsonify({"Meals Menu": menu_instance.menu}), 200


@menu.route('/menu', methods=['POST'])
@jwt_required
def set_menu():
    """View function to set menu"""
    if not check_admin():
        message = "Current user is not an admin"
        return jsonify({'message': message}), 400
    get_menu = request.get_json()

    menu_instance.create_menu(get_menu)

    return jsonify({"Menu": menu_instance.menu}), 201
