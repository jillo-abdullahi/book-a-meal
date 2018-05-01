"""test module for menu class"""
import unittest
import json

# Local import
from app import create_app
from app.v1.auth import user_instance


class TestMealsMenu(unittest.TestCase):
    """Test class for viewing for viewing and testing of menu"""

    def setUp(self):
        """Creates app with test client"""
        self.app = create_app("testing")
        self.app = self.app.test_client()
        self.new_meal = {"name": "Hamburger",
                         "description": "Tasty burger",
                         "price": "500",
                         "category": "main meal"}

    def test_customer_can_get_menu(self):
        """Function to test if customer can get menu"""
        register_response = self.register_user()
        self.assertEqual(register_response.status_code, 200)

        token = self.login_user()
        # We must add a meal first to generate menu
        response = self.app.post('/api/v1/meals',
                                 data=json.dumps(self.new_meal),
                                 headers={
                                     "content-type": "application/json",
                                     "Authorization": token})
        self.assertEqual(response.status_code, 200)

        # Menu must be set first for us to get it
        menu_response = self.set_menu()
        self.assertEqual(menu_response.status_code, 201)

        response = self.app.get('/api/v1/menu',
                                headers={
                                    "content-type": "application/json",
                                    "Authorization": token})
        self.assertEqual(response.status_code, 200)

    def test_caterer_can_set_menu(self):
        """Function to test if caterer can set menu"""
        register_response = self.register_user()
        self.assertEqual(register_response.status_code, 200)

        token = self.login_user()
        # We must add a meal first to generate menu
        response = self.app.post('/api/v1/meals',
                                 data=json.dumps(self.new_meal),
                                 headers={
                                     "content-type": "application/json",
                                     "Authorization": token})
        self.assertEqual(response.status_code, 200)
        # Setting menu
        menu_response = self.set_menu()

        self.assertEqual(menu_response.status_code, 201)

    def set_menu(self):
        """Function to set menu"""
        token = self.login_user()
        new_menu = {
            "1": {"name": "Hamburger"}
        }
        response = self.app.post('/api/v1/menu',
                                 data=json.dumps(new_menu),
                                 headers={
                                     "content-type": "application/json",
                                     "Authorization": token})
        return response

    def register_user(self):
        """Menu test - we need to register a user first"""
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

        access_token = json.loads(login_response.get_data(as_text=True))[
            "access_token"]

        headers = dict(Authorization="Bearer {}".format(access_token))
        return headers["Authorization"]
