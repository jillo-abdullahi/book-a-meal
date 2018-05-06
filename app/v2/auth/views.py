"""View functions for version 2 authorization routes"""
from flask import request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import re
from flask_jwt_extended import jwt_required, create_access_token


# local imports
from . import authV2
from app.models.modelsV2 import User
from app.utilities import check_keys, check_empty_dict, admin_required


@authV2.route("/signup", methods=["POST"])
def register_new_user():
    """View function to register a new user"""
    get_user = request.get_json()

    if check_keys(get_user, 4):
        message = "Please provide username, full-name, email and password"
        return jsonify({"message": message}), 400

    if check_empty_dict(get_user):
        message = "Some of your fields are empty, please rectify"
        return jsonify({"message": message}), 400

    try:
        username = get_user['username']
        email = get_user['email']
        password = generate_password_hash(
            get_user['password'], method='sha256')
        full_name = get_user['full-name']
    except Exception:
        message = "Please provide username, full-name, email and password"
        return jsonify({"message": message}), 400

    # Check if the username is valid
    username_regex = re.compile("^[A-Za-z0-9_-]{3,15}$")
    if not username_regex.match(username):
        message = "Username must have 3 to 15 characters and comprise only letters, numbers, an underscore or a hyphen"
        return jsonify({"Invalid username": message}), 400

    # Check if full name provided is valid
    full_name_regex = re.compile("^[A-Za-z\s]{4,30}$")
    if not full_name_regex.match(full_name):
        message = "Name must contain between 4 and 30 letters"
        return jsonify({"Invalid full name": message}), 400

    # Check if email provided is valid
    email_regex = re.compile("^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+.[a-zA-Z0-9-.]+$")
    if not email_regex.match(email):
        message = "Please enter a valid email address"
        return jsonify({"Invalid email": message}), 400

    # Check if the user exists first
    if User.query.filter_by(username=username).first():
        message = "Username, {} has already been taken".format(username)
        return jsonify({"message": message}), 400

    # Check if email has already been taken
    if User.query.filter_by(email=email).first():
        message = "A user with email, {} already exists".format(email)
        return jsonify({"message": message}), 400

    # Add the user to db once all checks passed
    user = User(username=username, full_name=full_name,
                email=email, password=password, admin=False)
    user.save()

    message = "Success! You have been registered"
    return jsonify({"message": message}), 201


@authV2.route('/login', methods=["POST"])
def login_user():
    """View function to log in a user"""
    get_user = request.get_json()

    if check_keys(get_user, 2):
        message = "Please provide a username and password"
        return jsonify({"message": message}), 400

    if check_empty_dict(get_user):
        message = "Some of your fields are empty, please rectify"
        return jsonify({"message": message}), 400

    username = get_user['username']
    password = get_user['password']

    try:
        user = User.query.filter_by(
            username=username).first()
        if check_password_hash(user.password, password):
            message = "Logged in as {}".format(username)
            access_token = create_access_token(
                identity={'user_id': user.id, 'admin': user.admin})

            return jsonify({"success": message, "access_token": access_token})
        return jsonify({"message": "Authentication failed, invalid username or password"}), 401
    except Exception:
        message = "Please provide a username and password"
        return jsonify({"message": message}), 400


@authV2.route('/promote/<user_id>', methods=["PUT"])
@jwt_required
def promote_user_to_admin(user_id):
    """View function to change a user to admin"""
    user = User.query.filter_by(id=user_id).first()
    if user:
        user.admin = True
        user.save()
        message = "{} promoted to admin".format(user.username)
        return jsonify({"message": message}), 200
    return jsonify({"message": "sorry, user doesn't exist"}), 404


@authV2.route('/users', methods=['GET'])
@jwt_required
@admin_required
def get_all_users():
    """View function to get all users"""
    current_users = User.query.all()
    return jsonify({"All users": [{'id': user.id, 'username': user.username} for user in current_users]}), 200
