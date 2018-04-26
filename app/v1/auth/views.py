# v1/auth/views.py


from flask_api import FlaskAPI
from flask import request, jsonify
from . import auth

all_users = []

@auth.route("/register", methods=["POST"])
def register_new_user():
	get_user = request.get_json()
	all_users.append(get_user)

	return jsonify({"message":"User successfully registered","Users":all_users}),201

@auth.route('/login', methods=["POST"])
def login_user():
	get_user = request.get_json()

	username = get_user["username"]
	password = get_user["password"]

	for user in all_users:
		if username == user["username"] and password == user["password"]:
			return jsonify({"user":user,"message":"User authenticated"}),200

	return jsonify({"message": "User was not found"}),404

