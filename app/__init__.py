# app/__init__.py

from flask_api import FlaskAPI
from flask import request, jsonify

from instance.config import app_config




def create_app(config_name):
	app = FlaskAPI(__name__, instance_relative_config=True)
	app.config.from_object(app_config[config_name])
	app.config.from_pyfile('config.py')

	# Register auth blueprint
	from .v1.auth import auth as auth_blueprint
	app.register_blueprint(auth_blueprint, url_prefix='/api/v1/auth')

	# Register meals blueprint
	from .v1.meals import meals as meals_blueprint
	app.register_blueprint(meals_blueprint, url_prefix='/api/v1')

	# Register menus blueprint
	from .v1.menu import menu as menu_blueprint
	app.register_blueprint(menu_blueprint, url_prefix='/api/v1')






	return app
