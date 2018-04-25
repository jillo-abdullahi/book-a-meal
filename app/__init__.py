from flask_api import FlaskAPI
from flask import request, jsonify

from instance.config import app_config

all_users = []

def create_app(config_name):
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    
    

    @app.route("/api/v1/auth/register", methods=["POST"])
    def register_new_user():
    	get_user = request.get_json()
    	all_users.append(get_user)

    	return jsonify({"message":all_users}),201

    @app.route('/api/v1/auth/login', methods=["POST"])
    def login_user():
    	get_user = request.get_json()

    	username = get_user["username"]
    	password = get_user["password"]

    	for user in all_users:
    		if username == user["username"] and password == user["password"]:
				return jsonify({"user":user,"message":"User authenticated"}),200

		return jsonify({"message": "User was not found"}),404

    return app
