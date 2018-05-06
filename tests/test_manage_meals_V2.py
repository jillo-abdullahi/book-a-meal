"""Test class for all things meal management"""
import unittest
import json

# Local imports
from app import create_app, db
from app.models.modelsV2 import User, Meals


class TestManageMeals(unittest.TestCase):
    """Test class for caterer ability to add,delete and update meals"""

    def setUp(self):
        """Creates the app with test client"""
        self.app = create_app("testing")
        self.client = self.app.app_context().push()
        self.client = self.app.test_client
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
        self.assertEqual(register_response.status_code, 201)

        token = self.login_user()

        response = self.client().post('/api/v2/meals',
                                      data=json.dumps(self.new_meal),
                                      headers={
                                          "content-type": "application/json",
                                          "Authorization": token})
        self.assertEqual(response.status_code, 201)

        # Get meal id to delete
        meal_added = Meals.query.filter_by(name=self.new_meal["name"]).first()
        meal_id = meal_added.id
        delete_response = self.client().delete('/api/v2/meals/{}'.format(meal_id),
                                               headers={
                                                   "content-type": "application/json",
                                                   "Authorization": token})

        self.assertEqual(delete_response.status_code, 200)

    def test_caterer_can_add_new_meal(self):
        """Function to test if a new meal can be added"""
        register_response = self.register_user()
        self.assertEqual(register_response.status_code, 201)

        token = self.login_user()
        response = self.client().post('/api/v2/meals',
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
        self.assertEqual(register_response.status_code, 201)

        token = self.login_user()

        # Add a meal to edit
        response = self.client().post('/api/v2/meals',
                                      data=json.dumps(self.new_meal),
                                      headers={
                                          "content-type": "application/json",
                                          "Authorization": token})
        self.assertEqual(response.status_code, 201)

        # Get meal id to edit
        meal_added = Meals.query.filter_by(name=self.new_meal["name"]).first()
        meal_id = meal_added.id

        edit_response = self.client().put('/api/v2/meals/{}'.format(meal_id),
                                          data=json.dumps(new_meal_details),
                                          headers={
                                              "content-type": "application/json",
                                              "Authorization": token})

        result = self.client().get('/api/v2/meals',
                                   headers={
                                       "content-type": "application/json",
                                       "Authorization": token})
        self.assertIn("Pepperoni", str(result.data))
        self.assertEqual(edit_response.status_code, 200)

    def register_user(self):
        """Meals test - we need to register a user first"""
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
            db.session.query(Meals).delete()
            db.session.commit()
