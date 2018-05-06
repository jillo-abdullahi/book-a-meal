"""View functions for all things meals"""
from flask import request, jsonify
from flask_jwt_extended import jwt_required


# local imports
from . import mealsV2
from app.models.modelsV2 import Meals
from app.utilities import check_keys, check_empty_dict, admin_required


@mealsV2.route("/meals", methods=["POST"])
@jwt_required
@admin_required
def caterer_add_new_meal():
    """View function to add a new meal"""
    get_meal = request.get_json()

    if check_keys(get_meal, 4):
        message = "Please provide a name, description, category and price for your meal"
        return jsonify({"message": message}), 400

    if check_empty_dict(get_meal):
        message = "Some of your fields are empty, please rectify"
        return jsonify({"message": message}), 400

    try:
        name = get_meal['name']
        price = get_meal['price']
        description = get_meal['description']
        category = get_meal['category']
    except:
        message = "Please provide a name, description, category and price for your meal"
        return jsonify({"message": message})

    try:
        meal = Meals(name=name, price=price,
                     description=description, category=category)
        meal.save()
        message = "Your meal has been successfully added"
        return jsonify({"message": message}), 201
    except Exception:
        message = "A meal with that name already exists"
        return jsonify({"message": message}), 400


@mealsV2.route("/meals", methods=["GET"])
@jwt_required
@admin_required
def caterer_get_all_meals():
    """View function to get all meals"""

    all_meals = Meals.query.all()
    if not all_meals:
        message = "No meals found"
        return jsonify({"message": message}), 404
    return jsonify({"All meals": [{'name': meal.name, 'description': meal.description, 'price': meal.price, 'category': meal.category, 'id': meal.id} for meal in all_meals]}), 200


@mealsV2.route("/meals/<meal_id>", methods=["DELETE"])
@jwt_required
@admin_required
def caterer_delete_meal(meal_id):
    """View function to delete a meal"""

    meal = Meals.query.filter_by(id=meal_id).first()
    if not meal:
        message = "Meal with id {} was not found".format(meal_id)
        return jsonify({"Error": message}), 404

    meal.delete()
    message = "meal successfully deleted"
    return jsonify({"message": message}), 200


@mealsV2.route("/meals/<meal_id>", methods=["PUT"])
@jwt_required
@admin_required
def caterer_edit_meal(meal_id):
    """View function to edit a meal option"""
    new_details = request.get_json()

    if check_keys(new_details, 4):
        message = "Please provide a name, description, category and price for your meal"
        return jsonify({"message": message}), 400

    if check_empty_dict(new_details):
        message = "Some of your fields are empty, please rectify"
        return jsonify({"message": message}), 400

    meal = Meals.query.filter_by(id=meal_id).first()
    if not meal:
        message = "Meal with id {} was not found".format(meal_id)
        return jsonify({"Error": message}), 404
    try:
        name = new_details['name']
        price = new_details['price']
        description = new_details['description']
        category = new_details['category']
    except Exception:
        message = "Please provide a name, description, category and price for your meal"
        return jsonify({"message": message}), 400

    meal.name = name
    meal.description = description
    meal.price = price
    meal.category = category

    meal.save()

    return jsonify({"message": "meal successfully updated"}), 200
