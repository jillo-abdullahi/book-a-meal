from flask_api import FlaskAPI
from flask import request, jsonify

from instance.config import app_config

all_users = []
all_meals = []

def create_app(config_name):
  app = FlaskAPI(__name__, instance_relative_config=True)
  app.config.from_object(app_config[config_name])
  app.config.from_pyfile('config.py')



  @app.route("/api/v1/auth/register", methods=["POST"])
  def register_new_user():
  	get_user = request.get_json()
  	all_users.append(get_user)

  	return jsonify({"message":"User successfully registered","Users":all_users}),201

  @app.route('/api/v1/auth/login', methods=["POST"])
  def login_user():
  	get_user = request.get_json()

  	username = get_user["username"]
  	password = get_user["password"]

  	for user in all_users:
  		if username == user["username"] and password == user["password"]:
			return jsonify({"user":user,"message":"User authenticated"}),200

	return jsonify({"message": "User was not found"}),404

  @app.route("/api/v1/meal", methods=["POST"])
  def add_new_meal():
    get_meal = request.get_json()
    get_meal["id"] = str(len(all_meals)+1)
    all_meals.append(get_meal)

    return jsonify({"message":"Meal successfully added","Meals":all_meals}),201

  @app.route("/api/v1/meals", methods=["GET"])
  def get_all_meals():

  	return jsonify({"Meals":all_meals}),200

  @app.route("/api/v1/meal/<id>", methods=["DELETE"])
  def delete_meal(id):
   	for meal in all_meals:
   		if id == meal["id"]:
   			all_meals.remove(meal)
   			return jsonify({"message":"Meal successfully removed"}),200
   	return jsonify({"message":"Meal not found"}),404

  @app.route("/api/v1/meal/<id>", methods=["PUT"])
  def edit_meal(id):
    new_details = request.get_json()

    for meal in all_meals:
      if id == meal["id"]:
        meal["name"] = new_details["name"]
        meal["description"] = new_details["description"]
        meal["price"] = new_details["price"]
        meal["category"] = new_details["category"]

        return jsonify({"message":"Meal successfully changed","Meal":meal}),200
    return jsonify({"message":"Meal not found"}),404

  return app
