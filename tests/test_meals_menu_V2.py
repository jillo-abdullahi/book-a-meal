"""test module for menu class"""
import unittest
import json

# Local import
from app import create_app, db
from app.models.modelsV2 import User, Meals, Menu


class TestMealsMenu(unittest.TestCase):
    """Test class for viewing for viewing and testing of menu"""

    def setUp(self):
        """Creates app with test client"""
        self.app = create_app("testing")
        self.client = self.app.app_context().push()
        self.client = self.app.test_client
        self.new_meal = {"name": "Hamburger",
                         "description": "Tasty burger",
                         "price": "500",
                         "category": "main meal"}

    def test_customer_can_get_menu(self):
        """Function to test if customer can get menu"""
        register_response = self.register_user()
        self.assertEqual(register_response.status_code, 201)

        token = self.login_user()

        # Menu must be set first for us to get it
        menu_response = self.set_menu()
        self.assertEqual(menu_response.status_code, 201)

        response = self.client().get('/api/v2/menu',
                                     headers={
                                         "content-type": "application/json",
                                         "Authorization": token})
        self.assertEqual(response.status_code, 200)

    def test_caterer_can_set_menu(self):
        """Function to test if caterer can set menu"""
        register_response = self.register_user()
        self.assertEqual(register_response.status_code, 201)

        # Setting menu
        menu_response = self.set_menu()

        self.assertEqual(menu_response.status_code, 201)

    def set_menu(self):
        """Function to set menu"""
        # We must add a meal first to generate menu
        token = self.login_user()
        response = self.client().post('/api/v2/meals',
                                      data=json.dumps(self.new_meal),
                                      headers={
                                          "content-type": "application/json",
                                          "Authorization": token})
        self.assertEqual(response.status_code, 201)

        # Get meal id to add
        meal = Meals.query.filter_by(name=self.new_meal["name"]).first()
        meal_id = meal.id

        new_menu = {"id": str(meal_id)}

        response = self.client().post('/api/v2/menu',
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
        response = self.client().post('/api/v2/auth/signup',
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
        user_instance = User.query.filter_by(
            username=user_login_info["username"]).first()
        user_instance.admin = True

        login_response = self.client().post('/api/v2/auth/login',
                                            data=json.dumps(user_login_info),
                                            content_type='application/json')

        access_token = json.loads(login_response.get_data(as_text=True))[
            "access_token"]

        headers = dict(Authorization="Bearer {}".format(access_token))
        return headers["Authorization"]

    def tearDown(self):
        with self.app.app_context():
            db.session.query(User).delete()
            db.session.commit()
            db.session.query(Menu).delete()
            db.session.commit()
            db.session.query(Meals).delete()
            db.session.commit()
