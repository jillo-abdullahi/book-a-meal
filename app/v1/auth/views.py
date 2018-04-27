"""v1/auth/views.py"""
from flask_api import FlaskAPI
from flask import request, jsonify

# local import
from . import auth, user_instance
from app.models.models import User
from app.utilities import check_keys, check_empty_dict

@auth.route("/signup", methods=["POST"])
def register_new_user():
	"""Register a new user"""
	get_user = request.get_json()

	if check_keys(get_user, 4):
		return jsonify({"message":"All fields must be provided"}),400

	if check_empty_dict(get_user):
		return jsonify({"message": "All fields must be provided"}),400

	all_users = user_instance.users
	for id in all_users:
		if get_user["username"].lower() == all_users[id]['username'].lower():
			return jsonify({"message":"user already exists"})
	user_instance.create_user(get_user)

	return jsonify({"message":"user successfully registered","Users":user_instance.users}),201

@auth.route('/login', methods=["POST"])
def login_user():
	"""Log a user in"""
	get_user = request.get_json()

	if check_keys(get_user, 2):
		return jsonify({"message":"All fields must be provided or provide just two"}),400

	if check_empty_dict(get_user):
		return jsonify({"message": "All fields must be provided"}),400

	all_users = user_instance.users

	for id in all_users:
		if get_user["username"] == all_users[id]["username"] and get_user["password"] == all_users[id]["password"]:
			return jsonify({"user":all_users[id],"message":"User authenticated"}),200

	return jsonify({"message": "User was not found"}),404

@auth.route('/promote/<user_id>', methods=["PUT"])
def promote_user_to_admin(user_id):

	if user_instance.promote_user(user_id):
		return jsonify({"message":"user has been promoted to admin"}),200
	return jsonify({"message":"sorry, user doesn't exist"}),404
