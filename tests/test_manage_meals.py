import unittest
import json

from app import create_app

class TestManageMeals(unittest.TestCase):
	"""Test class for caterer ability to add,delete and update meals"""

	def setUp(self):
		"""Creates the app as a test client"""
		self.app = create_app("testing")
		self.app = self.app.test_client()

	def test_meal_can_be_deleted_by_caterer(self):
		response = self.add_new_meal()

		delete_response = self.app.delete('/api/v1/meals/1')
		self.assertEqual(delete_response.status_code, 200)


	def test_caterer_can_add_new_meal(self):
		response = self.add_new_meal()
		self.assertEqual(response.status_code, 201)

	def test_caterer_can_edit_meal_item(self):

		new_meal_details = {"name": "Cheeseburger",
						"description":"Tasty burger",
						"price": "600",
						"category": "Todays special"}
		response = self.add_new_meal()
		self.assertEqual(response.status_code, 200)

		edit_response = self.app.put('/api/v1/meals/1',
			data = new_meal_details)

		# self.assertEqual(edit_response.status_code, 200)
		# result = self.app.get('/api/v1/meals/1')
		# self.assertIn("Todays special", str(result.data))


	def add_new_meal(self):
		new_meal_item = {"name": "Hamburger",
						"description":"Tasty burger",
						"price": "500",
						"category": "main meal"}
		response = self.app.post('/api/v1/meals',
			data = json.dumps(new_meal_item),
			content_type='application/json')
		return response
