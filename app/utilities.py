"""Functions for use in conducting various checks before proceeding"""
from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from functools import wraps


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


def admin_required(f):
    """Check if current user is admin"""
    @wraps(f)
    def decorated(*args, **kwargs):
        current_user = get_jwt_identity()
        if not current_user['admin']:
            return jsonify({"message": "Current user is not an admin"}), 400
    return decorated
