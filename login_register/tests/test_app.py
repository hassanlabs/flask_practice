import unittest
from app import create_app
from app.extensions import db

class BaseTestCase(unittest.TestCase):
    def setUp(self):
        """Set up a test client and create a new database for the test."""
        self.app = create_app('testing')  # Ensure you have a testing config
        self.client = self.app.test_client()
        
        with self.app.app_context():
            db.create_all()  # Create the database tables
    
    def tearDown(self):
        """Clean up the database after each test."""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

class UserAuthTests(BaseTestCase):
    
    def test_register(self):
        """Test user registration."""
        response = self.client.post('/register', json={
            'first_name': 'Hassan',
            'last_name': 'Tariq',
            'username': 'hassantariq',
            'email': 'hassan@example.com',
            'password': 'password123',
            'confirm_password': 'password123',
            'phone_number': '1234567890',
            'age': 25
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn(b'User registered successfully', response.data)

    def test_login(self):
        """Test user login."""
        # First register a user
        self.client.post('/register', json={
            'first_name': 'Hassan',
            'last_name': 'Tariq',
            'username': 'hassantariq',
            'email': 'hassan@example.com',
            'password': 'password123',
            'confirm_password': 'password123',
            'phone_number': '1234567890',
            'age': 25
        })
        
        # Now log in
        response = self.client.post('/login', json={
            'username': 'hassantariq',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login successful', response.data)

if __name__ == '__main__':
    unittest.main()
