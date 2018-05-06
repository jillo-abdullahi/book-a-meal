"""Test class for customer orders"""
import unittest
import json

# Local import
from app import create_app, db
from app.models.modelsV2 import User, Meals, Orders, Menu


class TestCustomerOrders(unittest.TestCase):
    """Test class for customer ability to place orders and also modify them"""

    def setUp(self):
        """Creates app with test client"""
        self.app = create_app("testing")
        self.client = self.app.app_context().push()
        self.client = self.app.test_client
        self.new_meal = {"name": "Hamburger",
                         "description": "Tasty burger",
                         "price": "500",
                         "category": "main meal"}
        with self.app.app_context():
            db.create_all()

    def test_customer_can_place_an_order(self):
        """Test if customer can place order"""
        register_response = self.register_user()
        self.assertEqual(register_response.status_code, 201)

        token = self.login_user()

        # Set the menu first to order from it
        menu_response = self.set_menu()
        self.assertEqual(menu_response.status_code, 201)

        # We then place order from the menu
        order_response = self.place_order()
        self.assertEqual(order_response.status_code, 201)

    def test_caterer_can_view_order_from_customer(self):
        """Test if caterer can view order"""

        register_response = self.register_user()
        self.assertEqual(register_response.status_code, 201)

        token = self.login_user()

        # Set the menu first
        menu_response = self.set_menu()
        self.assertEqual(menu_response.status_code, 201)

        order_response = self.place_order()
        self.assertEqual(order_response.status_code, 201)

        get_order = self.client().get('api/v2/orders',
                                      headers={
                                          "content-type": "application/json",
                                          "Authorization": token})
        self.assertEqual(get_order.status_code, 200)

    def place_order(self):
        """Method to place order for all tests"""
        token = self.login_user()
        new_order = {"name": "Hamburger"}
        response = self.client().post('api/v2/orders',
                                      data=json.dumps(new_order),
                                      headers={
                                          "content-type": "application/json",
                                          "Authorization": token})
        return response

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
        """Drop all tables after test has run"""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
