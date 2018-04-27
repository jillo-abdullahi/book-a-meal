# v1/meals/views.py

from flask_api import FlaskAPI
from flask import request, jsonify

# local imports
from . import meals, meal_instance
from app.models.models import Meals
from app.utilities import check_keys, check_empty_dict


@meals.route("/meals", methods=["POST"])
def caterer_add_new_meal():

	get_meal = request.get_json()

	if check_keys(get_meal, 4):
		return jsonify({"message":"All fields must be provided"}),400

	if check_empty_dict(get_meal):
		return jsonify({"message": "All fields must be provided"}),400


	all_meals = meal_instance.all_meals
	for id in all_meals:
		if get_meal["name"].lower() == all_meals[id]['name'].lower():
			return jsonify({"message":"Meal already exists"})

	meal_instance.create_meal(get_meal)

	return jsonify({"message":"Meal successfully added","Meals":meal_instance.all_meals}),201

@meals.route("/meals", methods=["GET"])
def caterer_get_all_meals():

	if not meal_instance.all_meals:
		return jsonify({"message":"No meals added yet"}),204
	return jsonify({"Meals":meal_instance.all_meals}),200

@meals.route("/meals/<id>", methods=["DELETE"])
def caterer_delete_meal(id):

	meals = meal_instance.all_meals
	for meal_id in meals:
		if id == meal_id:
			del(meals[id])
			return jsonify({"message":"Meal successfully removed","Meals":meal_instance.all_meals}),200
	return jsonify({"message":"Meal not found"}),404

@meals.route("/meals/<id>", methods=["PUT"])
def caterer_edit_meal(id):

	new_details = request.get_json()

	if check_keys(new_details, 4):
		return jsonify({"message":"All fields must be provided"}),400

	if check_empty_dict(new_details):
		return jsonify({"message": "All fields must be provided"}),400

	all_meals = meal_instance.all_meals
	for meal_id in all_meals:
		if id == meal_id:
			all_meals[id]["name"] = new_details["name"]
			all_meals[id]["description"] = new_details["description"]
			all_meals[id]["price"] = new_details["price"]
			all_meals[id]["category"] = new_details["category"]

			return jsonify({"message":"Meal successfully changed","Meal":meal_instance.all_meals[id]}),200
	return jsonify({"message":"Meal not found"}),404


