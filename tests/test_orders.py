import unittest
import json

from app import create_app


class TestCustomerOrders(unittest.TestCase):
    """Test class for customer ability to place orders and also modify them"""

    def setUp(self):
        self.app = create_app("testing")
        self.app = self.app.test_client()

    def test_customer_can_place_an_order(self):
        meals = self.add_new_meal()
        menu = self.set_menu()
        response = self.place_order()

        self.assertEqual(response.status_code, 201)

    def test_caterer_can_view_order_from_customer(self):
        meals = self.add_new_meal()
        menu = self.set_menu()
        response = self.place_order()

        get_order = self.app.get('api/v1/orders')
        self.assertEqual(get_order.status_code, 200)

    def test_customer_can_edit_order(self):
        updated_order = {"name": "Hamburger",
                         "description": "Tasty burger",
                                        "price": "500",
                                        "category": "main meal"}
        response = self.place_order()

        update_order = self.app.put('api/v1/orders/1',
                                    data=updated_order)
        self.assertEqual(update_order.status_code, 200)
        result = self.app.get('api/v1/orders/1')
        self.assertIn("Lemonade", str(result.data))

    def place_order(self):
        new_order = {
            "1": {"name": "Hamburger"}
        }
        response = self.app.post('api/v1/orders',
                                 data=json.dumps(new_order),
                                 content_type='application/json')
        return response

    def set_menu(self):
        new_menu = {
            "1": {"name": "Hamburger"}
        }
        response = self.app.post('/api/v1/menu',
                                 data=json.dumps(new_menu),
                                 content_type='application/json')
        return response

    def add_new_meal(self):
        new_meal_item = {"name": "Hamburger",
                         "description": "Tasty burger",
                                        "price": "500",
                                        "category": "main meal"}
        response = self.app.post('/api/v1/meals',
                                 data=json.dumps(new_meal_item),
                                 content_type='application/json')
        return response
