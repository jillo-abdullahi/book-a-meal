"""v1/auth/views.py"""
from flask import request, jsonify
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity


# local import
from . import auth
from . import user_instance
from app.utilities import check_keys, check_empty_dict, check_admin


@auth.route("/signup", methods=["POST"])
def register_new_user():
    """Register a new user"""
    get_user = request.get_json()

    if check_keys(get_user, 4):
        return jsonify({"message": "All fields must be provided"}), 400

    if check_empty_dict(get_user):
        return jsonify({"message": "All fields must be provided"}), 400

    all_users = user_instance.users
    for id in all_users:
        if get_user["username"].lower() == all_users[id]['username'].lower():
            return jsonify({"message": "user already exists"})
    user_instance.create_user(get_user)

    message = "user successfully registered"

    return jsonify({"message": message, "Users": user_instance.users}), 201


@auth.route('/login', methods=["POST"])
def login_user():
    """Log a user in"""
    get_user = request.get_json()

    if check_keys(get_user, 2):
        message = "All fields must be provided or provide just two"
        return jsonify({"message": message}), 400

    if check_empty_dict(get_user):
        return jsonify({"message": "All fields must be provided"}), 400

    all_users = user_instance.users

    for id in all_users:
        if get_user["username"] == all_users[id]["username"] and get_user["password"] == all_users[id]["password"]:

            access_token = create_access_token(identity=all_users[id])

            return jsonify({"user": all_users[id], "message": "User authenticated", "access_token": access_token}), 200

    return jsonify({"message": "User was not found"}), 404


@auth.route('/promote/<user_id>', methods=["PUT"])
@jwt_required
def promote_user_to_admin(user_id):
    """Function to change a user to admin"""
    if user_instance.promote_user(user_id):
        return jsonify({"message": "user has been promoted to admin"}), 200
    return jsonify({"message": "sorry, user doesn't exist"}), 404


@auth.route('/users', methods=['GET'])
@jwt_required
def get_all_users():
    """View function to get all users"""
    current_users = user_instance.users
    return jsonify({"All users": current_users}), 200
