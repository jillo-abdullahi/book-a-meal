"""V2/menu/views.py"""
from flask import request, jsonify
from flask_jwt_extended import jwt_required

# Local imports
from . import menuV2
from app.models.modelsV2 import Meals
from app.utilities import check_admin
from app.models.modelsV2 import Menu


@menuV2.route('/menu', methods=['POST'])
@jwt_required
def set_menu():
    """View function to set menu"""
    if not check_admin():
        message = "Current user is not an admin"
        return jsonify({'message': message}), 400

    menu_details = request.get_json()
    meal_id = int(menu_details['id'])

    # Check if meal exists
    meal = Meals.query.filter_by(id=meal_id).first()

    if not meal:
        message = "Meal cannot be added because it doesn't exist"
        return jsonify({"error": message})
    if Menu.query.filter_by(meal_id=meal_id).first():
        return jsonify({"message": "Meal already exists in the menu"})

    menu_item = Menu(name="breakfast", meal_id=meal.id)
    menu_item.save()

    message = "menu successfully updated"
    return jsonify({"message": message})


@menuV2.route('/menu', methods=['GET'])
@jwt_required
def get_meals_menu():
    """View function to get menu"""
    menu = Menu.query.all()
    if not menu:
        message = "Menu has not been set"
        return jsonify({"message": message}), 404

    meals_in_menu = []
    for menu_item in menu:
        meals_in_menu.append(menu_item.meal_id)
    all_meals = []

    for meal_id in meals_in_menu:
        meal = Meals.query.filter_by(id=meal_id).first()
        all_meals.append(
            {"name": meal.name, "price": meal.price, "category": meal.category,
             "description": meal.description})
    return jsonify({"message": all_meals}), 200
