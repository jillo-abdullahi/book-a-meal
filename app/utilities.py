"""Functions for use in conducting various checks before proceeding"""
from flask import jsonify
from functools import wraps
from flask_jwt_extended import get_jwt_identity


def check_keys(args, length):
    """Function to check if dict keys are provided"""
    params = ['email', 'username', 'password', 'full-name',
              'name', 'category', 'description', 'price', 'id']
    for key in args.keys():
        if key not in params or len(args) != length:
            return True
    return False


def check_empty_dict(args):
    """Function to check if an empty value's been given for any key"""
    for key in args:
        if not args[key].strip():
            return True
    return False


def check_admin():
    """Version 1 function to check if the current user is admin"""
    current_user = get_jwt_identity()
    if not current_user['admin']:
        return False
    return True


def admin_required(f):
    """Decorator function to check if current user is admin"""
    @wraps(f)
    def decorated(*args, **kwargs):
        current_user = get_jwt_identity()
        if not current_user['admin']:
            message = "Sorry, you are not an admin and therefore not allowed to access this page"
            return jsonify({"message": message}), 401
        return f(*args, **kwargs)
    return decorated
