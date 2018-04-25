from app import create_app
import unittest
import json

class TestCustomerOrders(unittest.TestCase):
	"""Test class for customer ability to place orders and also modify them"""
	def setUp(self):
		app.testing = True
		self.app = app.test_client()

	def test_customer_can_place_an_order(self):
		response = self.place_order()

		self.assertEqual(response.status_code, 201)

	def test_caterer_can_view_order_from_customer(self):
		response = self.place_order()

		get_order = self.app.get('api/v1/auth/order/1')
		self.assertEqual(get_order.status_code, 200)

	def test_customer_can_edit_order(self):
		updated_order = {"Hamburger": "600",
					"Lemonade": "200",
					"Chips":"150"}
		response = self.place_order()

		update_order = self.app.put('api/v1/auth/order/1',
			data = updated_order)
		self.assertEqual(update_order.status_code, 200)
		result = self.app.get('api/v1/auth/order/1')
		self.assertIn("Lemonade", str(result.data))

	def place_order(self):
		new_order = {"Hamburger": "600",
					"Diet Coke": "100",
					"Chips":"150"}
		response = self.app.post('api/v1/auth/order',
			data = json.dumps(new_order),
			content_type = 'application/json')
		return response

