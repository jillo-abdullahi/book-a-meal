"""orders/views.py"""
from flask import request, jsonify
from flask_jwt_extended import jwt_required,  get_jwt_identity

# local import
from . import ordersV2
from app.models.modelsV2 import Meals, Orders, Menu
from app.utilities import check_keys, check_empty_dict, check_admin


@ordersV2.route('/orders', methods=['GET'])
@jwt_required
def get_all_orders():
    """View function to get all orders for the day"""
    if not check_admin():
        message = "Current user is not an admin"
        return jsonify({'message': message}), 400
    current_orders = Orders.query.all()
    if not current_orders:
        message = "No orders have been placed yet."
        return jsonify({"message": message})
    meals_in_order = []

    for order in current_orders:
        meals_in_order.append(order.meals)
    all_meals = []

    for meal_id in meals_in_order:
        meal = Meals.query.filter_by(id=meal_id).first()
        all_meals.append({"name": meal.name, "price": meal.price})
    return jsonify({"message": all_meals}), 200


@ordersV2.route('/orders', methods=['POST'])
@jwt_required
def make_an_order():
    """View function to place an order"""
    get_order = request.get_json()

    meals_in_order = []

    for key in get_order:
        meals_in_order.append(get_order[key])

    for meal_in_order in meals_in_order:
        meal = Meals.query.filter_by(name=meal_in_order).first()
        if not meal:
            message = "{} is not an available meal".format(meal_in_order)
            return jsonify({"message": message}), 404
        menu = Menu.query.filter_by(meal_id=meal.id).first()
        if not menu:
            message = "{} is not part of today's menu".format(meal.name)
            return jsonify({"message": message}), 404
        current_user = get_jwt_identity()
        order = Orders(meals=meal.id, user_id=current_user["user_id"])
        order.save()

    return jsonify({"message": "order successfully updated"}), 201


@ordersV2.route('/orders/<order_id>', methods=['PUT'])
@jwt_required
def change_order(order_id):
    """View function to update an existing order"""
    new_order = request.get_json()

    meals_in_order = []

    order = Orders.query.filter_by(id=order_id).first()
    if not order:
        message = "There is no order with id {}".format(order_id)
        return jsonify({"message": message}), 404
    for key in new_order:
        meals_in_order.append(new_order[key])
    for meal_in_order in meals_in_order:
        meal = Meals.query.filter_by(name=meal_in_order).first()
        if not meal:
            message = "{} is not an available meal".format(meal_in_order)
            return jsonify({"message": message}), 404
        menu = Menu.query.filter_by(meal_id=meal.id).first()
        if not menu:
            message = "{} is not part of today's menu".format(meal.name)
            return jsonify({"message": message}), 404

        order.meals = meal.id
        order.save()

        message = "order successfully updated"
        return jsonify({"message": message})
