"""test module for menu class"""
import unittest
import json

from app import create_app


class TestMealsMenu(unittest.TestCase):
    """Test class for viewing for viewing and testing of menu"""

    def setUp(self):
        self.app = create_app("testing")
        self.app = self.app.test_client()

    def test_customer_can_get_menu(self):
        """Test customer can get meal for the day"""
        self.add_new_meal()
        self.set_menu()

        response = self.app.get('/api/v1/menu')
        self.assertEqual(response.status_code, 200)

    def test_caterer_can_set_menu(self):
        """Test caterer can set menu"""
        add_meal_first = self.add_new_meal()
        self.assertEqual(add_meal_first.status_code, 201)
        response = self.set_menu()

        self.assertEqual(response.status_code, 201)

    def set_menu(self):
        """Menu can be set after meal is added"""
        new_menu = {
            "1": {"name": "Hamburger"}
        }
        response = self.app.post('/api/v1/menu',
                                 data=json.dumps(new_menu),
                                 content_type='application/json')
        return response

    def add_new_meal(self):
        """Need to add meal in order to set menu"""
        new_meal_item = {"name": "Hamburger",
                         "description": "Tasty burger",
                         "price": "500",
                         "category": "main meal"}
        response = self.app.post('/api/v1/meals',
                                 data=json.dumps(new_meal_item),
                                 content_type='application/json')
        return response
