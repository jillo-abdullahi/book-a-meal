"""Test class for all things user"""
import unittest
import json

# Local imports
from app import create_app, db
from app.models.modelsV2 import User


class TestUserLogin(unittest.TestCase):
    """Test class for user login"""

    def setUp(self):
        """Creates the app with test client"""
        self.app = create_app("testing")
        self.client = self.app.app_context().push()
        self.client = self.app.test_client
        self.new_user_info = {
            "username": "test_user",
            "full-name": "Test User",
            "email": "testuser@gmail.com",
            "password": "password"
        }
        self.user_login_info = {
            "username": "test_user",
            "password": "password"
        }

    def test_successful_registration(self):
        """Test for successful registration"""
        response = self.register_user()
        self.assertEqual(response.status_code, 201)

    def test_successful_login(self):
        """Test for successful login"""
        self.register_user()
        response = self.login_user()
        self.assertEqual(response.status_code, 200)
        output = json.loads(response.get_data(as_text=True))['success']
        self.assertEqual(output, 'Logged in as test_user')

    def register_user(self):
        """Method for user registration"""
        response = self.client().post('/api/v2/auth/signup',
                                      data=json.dumps(self.new_user_info),
                                      content_type='application/json')
        return response

    def login_user(self):
        """Method for user log in"""
        response = self.client().post('/api/v2/auth/login',
                                      data=json.dumps(self.user_login_info),
                                      content_type='application/json')
        return response

    def tearDown(self):
        with self.app.app_context():
            db.session.query(User).delete()
            db.session.commit()
