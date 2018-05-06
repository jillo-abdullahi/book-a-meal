"""View functions for all things menu"""
from flask import request, jsonify
from flask_jwt_extended import jwt_required

# Local imports
from . import menuV2
from app.models.modelsV2 import Meals
from app.utilities import admin_required, check_empty_dict, check_keys
from app.models.modelsV2 import Menu


@menuV2.route('/menu', methods=['POST'])
@jwt_required
@admin_required
def set_menu():
    """View function to set menu"""

    menu_details = request.get_json()

    if check_keys(menu_details, 1):
        message = "Please provide just the meal id"
        return jsonify({"message": message}), 400

    if check_empty_dict(menu_details):
        message = "Please fill in the id field"
        return jsonify({"message": message}), 400
    try:
        meal_id = int(menu_details['id'])
    except Exception:
        message = "Please specify a meal id to add to the menu"
        return jsonify({"message": message}), 400

    # Check if meal exists
    meal = Meals.query.filter_by(id=meal_id).first()

    if not meal:
        message = "Meal cannot be added because it doesn't exist"
        return jsonify({"error": message})
    if Menu.query.filter_by(meal_id=meal_id).first():
        return jsonify({"message": "Meal already exists in the menu"})

    menu_item = Menu(name="Today's Menu", meal_id=meal.id)
    menu_item.save()

    message = "menu successfully updated"
    return jsonify({"message": message}), 201


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
