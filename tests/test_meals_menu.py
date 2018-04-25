from app import app
import unittest
import json

class TestMealsMenu(unittest.TestCase):
	"""Test class for viewing of menu by customers and setting of menu by caterer"""
	def setUp(self):
		app.testing = True
		self.app = app.test_client()


	def test_customer_can_get_menu_for_specific_day(self):
		response = self.set_menu()

		get_menu = self.app.get('/api/v1/auth/menu')
		self.assertEqual(get_menu.status_code, 200)

	def test_caterer_can_set_menu_for_the_day(self):
		response = self.set_menu()

		self.assertEqual(response.status_code, 201)
		self.assertEqual(response.status_code, 200)


	def set_menu(self):
		new_menu = {
		"main-meal":["Pizza","Hamburger", "Chips"],
		"drinks": ["Chocolate milkshake","lemonade"],
		"desserts": ["Vanilla ice cream", "chocolate pudding"],
		"todays-special": ["shawarma","special chips"]
		}
		response = self.app.post('/api/v1/auth/menu',
			data = json.dumps(new_menu),
			content_type = 'application/json')
		return response
