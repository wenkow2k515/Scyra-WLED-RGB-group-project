import unittest
from flask import url_for
from app import create_app, db
from app.models import User
from werkzeug.security import generate_password_hash

class AuthTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up the Flask app and database for testing."""
        cls.app = create_app('testing')  # Use the TestingConfig
        cls.app_context = cls.app.app_context()
        cls.app_context.push()
        cls.client = cls.app.test_client()
        db.create_all()

    @classmethod
    def tearDownClass(cls):
        """Tear down the Flask app and database."""
        db.session.remove()
        db.drop_all()
        cls.app_context.pop()

    def setUp(self):
        """Set up test data."""
        # Add a test user to the database
        hashed_password = generate_password_hash('bruh')
        test_user = User(email='bruhh@bruh.com', password=hashed_password, fname='bruh', lname='bruh')
        db.session.add(test_user)
        db.session.commit()

    def tearDown(self):
        """Clean up after each test."""
        db.session.query(User).delete()
        db.session.commit()

    def test_register_success(self):
        """Test successful user registration."""
        response = self.client.post('/register', data={
            'email': 'bruh@bruh.com',
            'fname': 'bruh',
            'lname': 'bruh',
            'password': 'bruh',
            'confirm_password': 'bruh',
            'secret_question': "What was your first pet's name?",
            'secret_answer': 'bruh'
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Your account has been created!', response.data)

        # Verify the user was added to the database
        user = User.query.filter_by(email='bruh@bruh.com').first()
        self.assertIsNotNone(user)
        self.assertEqual(user.fname, 'bruh')
        self.assertEqual(user.lname, 'bruh')

    def test_register_failure(self):
        """Test registration failure due to mismatched passwords."""
        response = self.client.post('/register', data={
            'email': 'bruh@bruh.com',
            'fname': 'bruh',
            'lname': 'bruh',
            'password': 'bruh',
            'confirm_password': 'wrongpassword',
            'secret_question': "What was your first pet's name?",
            'secret_answer': 'bruh'
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Passwords must match.', response.data)

    def test_login_success(self):
        """Test successful login."""
        response = self.client.post('/login', data={
            'email': 'bruhh@bruh.com',
            'password': 'bruh'
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login successful!', response.data)

    def test_login_failure(self):
        """Test login failure with incorrect credentials."""
        response = self.client.post('/login', data={
            'email': 'bruhh@bruh.com',
            'password': 'wrongpassword'
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login unsuccessful. Please check email and password', response.data)

    def test_login_redirect(self):
        """Test login redirects to the account page."""
        response = self.client.post('/login', data={
            'email': 'bruhh@bruh.com',
            'password': 'bruh'
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Account', response.data)

if __name__ == '__main__':
    unittest.main()