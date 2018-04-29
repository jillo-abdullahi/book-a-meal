"""orders/views.py"""
from flask import request, jsonify

# local import
from . import orders, orders_instance


@orders.route('/orders', methods=['GET'])
def get_all_orders():
    """get all orders for the day"""
    if not orders_instance.orders:
        return jsonify({"message": "No orders found"}), 204
        return jsonify({"Orders": orders_instance.orders}), 200


@orders.route('/orders', methods=['POST'])
def make_an_order():
    """Customer can place an order"""
    get_order = request.get_json()

    orders_instance.create_order(get_order)

    return jsonify({"Orders": orders_instance.orders}), 201


@orders.route('/orders/<id>', methods=['PUT'])
def change_order(id):
    """Customer can change an order"""
    new_order = request.get_json()

    # if check_keys(new_order, 4):
    # 	return jsonify({"message":"All fields must be provided"}),400

    # if check_empty_dict(new_order):
    # 	return jsonify({"message": "All fields must be provided"}),400

    all_orders = orders_instance.orders
    for order_id in all_orders:
        if id == order_id:
            all_orders[id]["name"] = new_order["name"]
            all_orders[id]["category"] = new_order["category"]
            all_orders[id]["price"] = new_order["price"]
            all_orders[id]["description"] = new_order["description"]

            return jsonify({"message": "order details successfully changed", "Order": orders_instance.orders}), 200
    return jsonify({"message": "Order with that id was not found"}), 404
