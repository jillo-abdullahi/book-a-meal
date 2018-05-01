"""Test class for all things meal management"""
import unittest
import json

# Local import
from app import create_app
from app.v1.auth import user_instance


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
        """Function to test if caterer can delete a meal"""
        register_response = self.register_user()
        self.assertEqual(register_response.status_code, 200)

        token = self.login_user()

        response = self.app.post('/api/v1/meals',
                                 data=json.dumps(self.new_meal),
                                 headers={
                                     "content-type": "application/json",
                                     "Authorization": token})
        self.assertEqual(response.status_code, 201)
        delete_response = self.app.delete('/api/v1/meals/1',
                                          headers={
                                              "content-type": "application/json",
                                              "Authorization": token})

        self.assertEqual(delete_response.status_code, 200)

    def test_caterer_can_add_new_meal(self):
        """Function to test if a new meal can be added"""
        register_response = self.register_user()
        self.assertEqual(register_response.status_code, 201)

        token = self.login_user()
        response = self.app.post('/api/v1/meals',
                                 data=json.dumps(self.new_meal),
                                 headers={
                                     "content-type": "application/json",
                                     "Authorization": token})
        self.assertEqual(response.status_code, 201)

    def test_caterer_can_edit_meal_item(self):
        """Function to test if caterer can edit a meal"""
        new_meal_details = {"name": "Pizza",
                            "description": "Pepperoni is awesome!",
                            "price": "500",
                            "category": "main meal"}
        # Register the user first, login to get an admin token
        register_response = self.register_user()
        self.assertEqual(register_response.status_code, 200)

        token = self.login_user()
        edit_response = self.app.put('/api/v1/meals/1',
                                     data=json.dumps(new_meal_details),
                                     headers={
                                         "content-type": "application/json",
                                         "Authorization": token})

        result = self.app.get('/api/v1/meals',
                              headers={
                                  "content-type": "application/json",
                                  "Authorization": token})
        self.assertIn("Pepperoni", str(result.data))

    def register_user(self):
        """Meals test - we need to register a user first"""
        new_user_info = {
            "username": "zayn",
            "full-name": "Zayn Malik",
            "email": "jayloabdullahi@gmail.com",
            "password": "check1234",
        }
        response = self.app.post('/api/v1/auth/signup',
                                 data=json.dumps(new_user_info),
                                 content_type='application/json')
        return response

    def login_user(self):
        """Meals test - login the user to generate a token"""
        user_login_info = {
            "username": "zayn",
            "password": "check1234"
        }
        # Promote current user to admin
        user_instance.users['1']['admin'] = True

        login_response = self.app.post('/api/v1/auth/login',
                                       data=json.dumps(user_login_info),
                                       content_type='application/json')

        access_token = json.loads(login_response.data)["access_token"]

        headers = dict(Authorization="Bearer {}".format(access_token))
        return headers['Authorization']
