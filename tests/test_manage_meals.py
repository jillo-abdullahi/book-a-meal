"""Test class for all things meal management"""
import unittest
import json

# Local import
from app import create_app


class TestManageMeals(unittest.TestCase):
    """Test class for caterer ability to add,delete and update meals"""

    def setUp(self):
        """Creates the app with test client"""
        self.app = create_app("testing")
        self.app = self.app.test_client()
        self.new_meal = {"name": "Hamburger",
                         "description": "Tasty burger",
                                        "price": "500",
                                        "category": "main meal"}

        self.edit_meal = {"name": "Veggieburger",
                          "description": "burger",
                          "price": "200",
                          "category": "main meal"}

    def test_meal_can_be_deleted_by_caterer(self):
        self.add_new_meal(self.new_meal)

        delete_response = self.app.delete('/api/v1/meals/1')
        self.assertEqual(delete_response.status_code, 200)

    def test_caterer_can_add_new_meal(self):
        response = self.add_new_meal(self.new_meal)
        self.assertEqual(response.status_code, 201)

        # delete the meal we just created

    def test_caterer_can_edit_meal_item(self):
        # new_meal_details = {"name": "Pizza",
        #                     "description": "Pepperoni is awesome!",
        #                     "price": "500",
        #                     "category": "main meal"}

        response = self.add_new_meal(self.edit_meal)
        print(response.data)
        self.assertEqual(response.status_code, 201)

        # edit_response = self.app.put('/api/v1/meals/1',
        # 	data = new_meal_details)

        # self.assertEqual(edit_response.status_code, 200)
        # result = self.app.get('/api/v1/meals/1')
        # self.assertIn("Todays special", str(result.data))

    def add_new_meal(self, meal_item):
        response = self.app.post('/api/v1/meals',
                                 data=json.dumps(meal_item),
                                 content_type='application/json')
        return response


if __name__ == "__main__":
    unittest.main()
