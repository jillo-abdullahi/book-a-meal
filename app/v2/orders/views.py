"""View functions for all things orders"""
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

# local import
from . import ordersV2
from app.models.modelsV2 import Meals, Orders, Menu
from app.utilities import check_keys, check_empty_dict, admin_required


@ordersV2.route('/orders', methods=['GET'])
@jwt_required
@admin_required
def get_all_orders():
    """View function to get all orders for the day"""

    current_orders = Orders.query.all()
    if not current_orders:
        message = "No orders have been placed yet."
        return jsonify({"message": message})

    meals_in_order = []
    for order in current_orders:
        meals_in_order.append(order.meals)
    all_meals = []
    for meal_id in meals_in_order:
        order_status = Orders.query.filter_by(
            meals=meal_id, complete=False).first()
        meal = Meals.query.filter_by(id=meal_id).first()
        all_meals.append({"meal": meal.name, "price": meal.price,
                          "complete": order_status.complete, "customer": order_status.user_id, "time": order_status.date_created, "order_id": order_status.id})
    return jsonify({"Unfilled orders": all_meals}), 200


@ordersV2.route('/orders', methods=['POST'])
@jwt_required
def make_an_order():
    """View function to place an order"""

    get_order = request.get_json()
    if check_keys(get_order, 1):
        message = "Please provide a meal name"
        return jsonify({"message": message}), 400
    if check_empty_dict(get_order):
        message = "Meal name has not been specified"
        return jsonify({"message": message}), 400

    try:
        meal_ordered = get_order["name"]
    except Exception:
        message = "Please provide a meal name"
        return jsonify({"message": message}), 400

    meal = Meals.query.filter_by(name=meal_ordered).first()
    if not meal:
        message = "{} is not an available meal".format(meal_ordered)
        return jsonify({"message": message}), 404
    menu = Menu.query.filter_by(meal_id=meal.id).first()
    if not menu:
        message = "{} is not part of today's menu".format(meal.name)
        return jsonify({"message": message}), 404
    current_user = get_jwt_identity()
    order = Orders(meals=meal.id, user_id=current_user[
                   "user_id"], complete=False)
    order.save()

    return jsonify({"message": "order successfully updated"}), 201


@ordersV2.route('/orders/<order_id>', methods=['PUT'])
@jwt_required
def change_order(order_id):
    """View function to update an existing order"""
    new_order = request.get_json()

    if check_keys(new_order, 1):
        message = "Please provide a meal name"
        return jsonify({"message": message}), 400
    if check_empty_dict(new_order):
        message = "Meal name has not been specified"
        return jsonify({"message": message}), 400

    try:
        meal_in_order = new_order["name"]
    except Exception:
        message = "Please provide a meal name"
        return jsonify({"message": message}), 400

    order = Orders.query.filter_by(id=order_id).first()
    if not order:
        message = "There is no order with id {}".format(order_id)
        return jsonify({"message": message}), 404

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
