"""app/__init__.py"""
import os
from flask import render_template
from flask_api import FlaskAPI
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy

# local import
from instance.config import app_config

db = SQLAlchemy()


def create_app(config_name):
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.url_map.strict_slashes = False
    db.init_app(app)

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

    # Blueprints for version 2:

    # Register auth blueprint
    from .v2.auth import authV2 as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/api/v2/auth')

    # Register meals blueprint
    from .v2.meals import mealsV2 as meals_blueprint
    app.register_blueprint(meals_blueprint, url_prefix='/api/v2')

    # Register menus blueprint
    from .v2.menu import menuV2 as menu_blueprint
    app.register_blueprint(menu_blueprint, url_prefix='/api/v2')

    # Register orders blueprint
    from .v2.orders import ordersV2 as orders_blueprint
    app.register_blueprint(orders_blueprint, url_prefix='/api/v2')

    @app.route('/')
    @app.route('/favicon.ico')
    def api_documentation():
        """route for API documentation"""
        return render_template('version1.html')

    return app
