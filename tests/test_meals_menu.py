from app import create_app
import unittest
import json

class TestMealsMenu(unittest.TestCase):
	"""Test class for viewing of menu by customers and setting of menu by caterer"""
	def setUp(self):
		self.app = create_app("testing")
		self.app = self.app.test_client()


	def test_customer_can_get_menu_for_specific_day(self):
		add_new_meal_first = self.add_new_meal()
		set_menu_first = self.set_menu()

		response = self.app.get('/api/v1/menu')
		self.assertEqual(response.status_code, 200)

	def test_caterer_can_set_menu_for_the_day(self):
		add_meal_first = self.add_new_meal()
		self.assertEqual(add_meal_first.status_code, 201)
		response = self.set_menu()

		self.assertEqual(response.status_code, 201)

	def set_menu(self):
		new_menu = {
					"1":{"name": "Hamburger"}
					}
		response = self.app.post('/api/v1/menu',
			data = json.dumps(new_menu),
			content_type = 'application/json')
		return response

	def add_new_meal(self):
		new_meal_item = {"name": "Hamburger",
						"description":"Tasty burger",
						"price": "500",
						"category": "main meal"}
		response = self.app.post('/api/v1/meals',
			data = json.dumps(new_meal_item),
			content_type='application/json')
		return response
