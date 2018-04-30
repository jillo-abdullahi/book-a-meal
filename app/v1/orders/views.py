"""orders/views.py"""
from flask import request, jsonify
from flask_jwt_extended import jwt_required

# local import
from . import orders, orders_instance
from app.utilities import check_admin


@orders.route('/orders', methods=['GET'])
@jwt_required
def get_all_orders():
    """get all orders for the day"""
    if not check_admin():
        message = "Current user is not an admin"
        return jsonify({'message': message}), 400

    if not orders_instance.orders:
        return jsonify({"message": "No orders found"}), 404
    return jsonify({"Orders": orders_instance.orders}), 200


@orders.route('/orders', methods=['POST'])
@jwt_required
def make_an_order():
    """Customer can place an order"""
    get_order = request.get_json()

    orders_instance.create_order(get_order)

    return jsonify({"Orders": orders_instance.orders}), 201


@orders.route('/orders/<id>', methods=['PUT'])
@jwt_required
def change_order(id):
    """Customer can change an order"""
    new_order = request.get_json()

    all_orders = orders_instance.orders

    for order_id in all_orders:
        if id == order_id:
            all_orders[id]["name"] = new_order["name"]
            all_orders[id]["category"] = new_order["category"]
            all_orders[id]["price"] = new_order["price"]
            all_orders[id]["description"] = new_order["description"]

            return jsonify({"message": "order details successfully changed", "Order": orders_instance.orders}), 200
    return jsonify({"message": "Order with that id was not found"}), 404
