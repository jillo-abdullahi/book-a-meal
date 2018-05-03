"""v2/auth/views.py"""
from flask import request, jsonify
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity


# local import
from . import authV2
from app.models.modelsV2 import User
from app.utilities import check_keys, check_empty_dict


@authV2.route("/signup", methods=["POST"])
def register_new_user():
    """Register a new user"""
    get_user = request.get_json()

    if check_keys(get_user, 4):
        return jsonify({"message": "All fields must be provided"}), 400

    if check_empty_dict(get_user):
        return jsonify({"message": "All fields must be provided"}), 400

    try:
        username = get_user['username']
        email = get_user['email']
        password = get_user['password']
        full_name = get_user['full-name']
    except Exception:
        return jsonify({"message": "All fields must be provided"}), 400

    # Add the user to db
    user = User(username=username, full_name=full_name,
                email=email, password=password, admin=False)
    user.save()

    message = "User successfully registered"
    return jsonify({"message": message}), 200


@authV2.route('/login', methods=["POST"])
def login_user():
    """Log a user in"""
    get_user = request.get_json()

    if check_keys(get_user, 2):
        message = "All fields must be provided or provide just two"
        return jsonify({"message": message}), 400

    if check_empty_dict(get_user):
        return jsonify({"message": "All fields must be provided"}), 400

    username = get_user['username']
    password = get_user['password']

    try:
        user = User.query.filter_by(
            username=username, password=password).first()
        if user:
            message = "user successfully logged in"
            access_token = create_access_token(
                identity={'user_id': user.id, 'admin': user.admin})

            return jsonify({"message": message, "access_token": access_token})
        return jsonify({"message": "Authentication failed, please try again"})
    except Exception:
        return jsonify({"message": "All fields must be provided"}), 400


@authV2.route('/promote/<user_id>', methods=["PUT"])
@jwt_required
def promote_user_to_admin(user_id):
    """Function to change a user to admin"""
    user = User.query.filter_by(id=user_id).first()
    if user:
        user.admin = True
        user.save()
        return jsonify({"message": "user has been promoted to admin"}), 200
    return jsonify({"message": "sorry, user doesn't exist"}), 404


@authV2.route('/users', methods=['GET'])
@jwt_required
def get_all_users():
    """View function to get all users"""
    current_users = User.query.all()
    return jsonify({"All users": [{'id': user.id, 'username': user.username} for user in current_users]}), 200
