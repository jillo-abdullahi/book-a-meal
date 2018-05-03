# v2/meals/views.py
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity


# local import
from . import mealsV2
from app.models.modelsV2 import Meals
from app.utilities import check_keys, check_empty_dict, check_admin


@mealsV2.route("/meals", methods=["POST"])
@jwt_required
def caterer_add_new_meal():
    """Test caterer can add new meal"""
    get_meal = request.get_json()

    if check_keys(get_meal, 4):
        return jsonify({"message": "All fields must be provided"}), 400

    if check_empty_dict(get_meal):
        return jsonify({"message": "All fields must be provided"}), 400

    if not check_admin():
        message = "Current user is not an admin"
        return jsonify({'message': message}), 400

    name = get_meal['name']
    price = get_meal['price']
    description = get_meal['description']
    category = get_meal['category']

    try:
        meal = Meals(name=name, price=price,
                     description=description, category=category)
        meal.save()
        message = "meal successfully added"
        return jsonify({"message": message}), 201
    except Exception:
        return jsonify({"message": "All fields must be provided"}), 400


@mealsV2.route("/meals", methods=["GET"])
@jwt_required
def caterer_get_all_meals():
    """Method to get all meals"""
    if not check_admin():
        message = "Current user is not an admin"
        return jsonify({'message': message}), 400

    all_meals = Meals.query.all()
    if not all_meals:
        message = "No meals found"
        return jsonify({"message": message}), 404
    return jsonify({"All meals": [{'name': meal.name, 'description': meal.description, 'price': meal.price, 'category': meal.category} for meal in all_meals]}), 200


@mealsV2.route("/meals/<meal_id>", methods=["DELETE"])
@jwt_required
def caterer_delete_meal(meal_id):
    """Method to delete a meal"""
    if not check_admin():
        message = "Current user is not an admin"
        return jsonify({'message': message}), 400

    meal = Meals.query.filter_by(id=meal_id).first()
    if not meal:
        message = "Meal with id {} was not found".format(meal_id)
        return jsonify({"Error": message})

    meal.delete()
    message = "meal successfully deleted"
    return jsonify({"message": message})


@mealsV2.route("/meals/<meal_id>", methods=["PUT"])
@jwt_required
def caterer_edit_meal(meal_id):
    """Method to edit a meal option"""
    new_details = request.get_json()

    if not check_admin():
        message = "Current user is not an admin"
        return jsonify({'message': message}), 400

    if check_keys(new_details, 4):
        return jsonify({"message": "All fields must be provided"}), 400

    if check_empty_dict(new_details):
        return jsonify({"message": "All fields must be provided"}), 400

    meal = Meals.query.filter_by(id=meal_id).first()
    if not meal:
        message = "Meal with id {} was not found".format(meal_id)
        return jsonify({"Error": message})

    name = new_details['name']
    price = new_details['price']
    description = new_details['description']
    category = new_details['category']

    meal.name = name
    meal.description = description
    meal.price = price
    meal.category = category

    meal.save()

    return jsonify({"message": "meal successfully updated"}), 200
