from app import create_app
import unittest
import json

class TestUserLogin(unittest.TestCase):
	"""Test class for user login"""
	def setUp(self):
		"""Creates the app as a test client"""
		app.testing = True
		self.app = app.test_client()
		
	def test_successful_registration(self):
		response = self.register_user()
		self.assertEqual(response.status_code, 201)
		self.assertEqual(response.status_code, 200)


	def test_successful_login(self):
		response = self.login_user()
		self.assertEqual(response.status_code, 200)
		output = json.loads(response.get_data(as_text=True))['message']
		self.assertEqual(output, 'Login success')

	def register_user(self):
		new_user_info = {
            "username":"zayn",
            "full-name":"Zayn Malik",
            "email":"jayloabdullahi@gmail.com",
            "password":"check1234"
            }
		response = self.app.post('/api/v1/auth/register',
			data = json.dumps(new_user_info),
			content_type='application/json')
		return response

	def login_user(self):
		user_login_info = {
			"username":"zayn",
			"password":"check1234"
			}
		response = self.app.post('/api/v1/auth/login',
			data = json.dumps(user_login_info),
			content_type='application/json')
		return response


if __name__ == "__main__":
	unittest.main()

