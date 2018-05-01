"""Test class for all things user"""
import unittest
import json

# Local import
from app import create_app


class TestUserLogin(unittest.TestCase):
    """Test class for user login"""

    def setUp(self):
        """Creates the app with test client"""
        self.app = create_app("testing")
        self.app = self.app.test_client()

    def test_successful_registration(self):
        """Test for successful registration"""
        response = self.register_user()
        self.assertEqual(response.status_code, 200)

    def test_successful_login(self):
        """Test for successful login"""
        self.register_user()
        response = self.login_user()
        self.assertEqual(response.status_code, 200)
        output = json.loads(response.get_data(as_text=True))['message']
        self.assertEqual(output, 'User authenticated')

    def register_user(self):
        """Method for user registration"""
        new_user_info = {
            "username": "zayn",
            "full-name": "Zayn Malik",
            "email": "jayloabdullahi@gmail.com",
            "password": "check1234"
        }
        response = self.app.post('/api/v1/auth/signup',
                                 data=json.dumps(new_user_info),
                                 content_type='application/json')
        return response

    def login_user(self):
        """Method for user log in"""
        user_login_info = {
            "username": "zayn",
            "password": "check1234"
        }
        response = self.app.post('/api/v1/auth/login',
                                 data=json.dumps(user_login_info),
                                 content_type='application/json')
        return response
