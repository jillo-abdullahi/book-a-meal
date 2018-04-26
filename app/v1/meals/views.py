# v1/meals/views.py

from flask_api import FlaskAPI
from flask import request, jsonify
from . import meals

all_meals = []

@meals.route("/meal", methods=["POST"])
def caterer_add_new_meal():
	get_meal = request.get_json()
	get_meal["id"] = str(len(all_meals)+1)

	all_meals.append(get_meal)

	return jsonify({"message":"Meal successfully added","Meals":all_meals}),201

@meals.route("/meals", methods=["GET"])
def caterer_get_all_meals():

	return jsonify({"Meals":all_meals}),200

@meals.route("/meal/<id>", methods=["DELETE"])
def caterer_delete_meal(id):
	for meal in all_meals:
		if id == meal["id"]:
			all_meals.remove(meal)
			return jsonify({"message":"Meal successfully removed"}),200
	return jsonify({"message":"Meal not found"}),404

@meals.route("/meal/<id>", methods=["PUT"])
def caterer_edit_meal(id):

	new_details = request.get_json()

	for meal in all_meals:
		if id == meal["id"]:
			meal["name"] = new_details["name"]
			meal["description"] = new_details["description"]
			meal["price"] = new_details["price"]
			meal["category"] = new_details["category"]

		return jsonify({"message":"Meal successfully changed","Meal":meal}),200
	return jsonify({"message":"Meal not found"}),404
