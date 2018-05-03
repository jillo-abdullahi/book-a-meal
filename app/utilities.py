"""Functions for use in conducting various checks before proceeding"""
import re
from flask import jsonify
from flask_jwt_extended import get_jwt_identity


def check_keys(args, length):
    """Check if dict keys are provided"""
    params = ['email', 'username', 'password', 'full-name',
              'name', 'category', 'description', 'price']
    for key in args.keys():
        if key not in params or len(args) != length:
            return True
    return False


def check_empty_dict(args):
    """Check if an empty value given for any key"""
    for key in args:
        if not args[key].strip():
            return True
    return False


def check_admin():
    """Check if current user is admin"""
    current_user = get_jwt_identity()
    if not current_user['admin']:
        return False
    return True


# validations
username_regex = re.compile("^[a-z0-9_-]{3,15}$")
password_regex = re.compile("^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{6,}$")
email_regex = re.compile("[^@]+@[^@]+\.[^@]+")


def validate(data):
    """Validate email password and username
    """
    if check_keys(data, 3):
        return jsonify({
            'warning': 'Provide email, username & password'
        }), 400

    if not data['email'] or not data['password'] or not data['username']:
        return jsonify({
            'warning': 'Cannot create user without all information'
        }), 400

    if not username_regex.match(data['username']):
        return jsonify({
            'warning': 'Provide username with more than 4 characters'
        })

    if not email_regex.match(data['email']):
        return jsonify({
            'warning': 'Please provide valid email'
        })

    if not password_regex.match(data['password']):
        return jsonify({
            'warning': 'Please provide strong password'
        })
