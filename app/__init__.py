"""app/__init__.py"""
import os
from flask import render_template
from flask_api import FlaskAPI
from flask_jwt_extended import JWTManager

# local import
from instance.config import app_config


def create_app(config_name):
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')

    app.config['JWT_SECRET_KEY'] = os.getenv('SECRET')
    jwt = JWTManager(app)

    # Register auth blueprint
    from .v1.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/api/v1/auth')

    # Register meals blueprint
    from .v1.meals import meals as meals_blueprint
    app.register_blueprint(meals_blueprint, url_prefix='/api/v1')

    # Register menus blueprint
    from .v1.menu import menu as menu_blueprint
    app.register_blueprint(menu_blueprint, url_prefix='/api/v1')

    # Register orders blueprint
    from .v1.orders import orders as orders_blueprint
    app.register_blueprint(orders_blueprint, url_prefix='/api/v1')

    @app.route('/')
    @app.route('/favicon.ico')
    def api_documentation():
        """route for API documentation"""
        return render_template('version1.html')

    return app
