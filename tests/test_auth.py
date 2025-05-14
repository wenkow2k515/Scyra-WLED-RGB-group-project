import unittest
from app import create_app, db
from app.models import User
from tests.controllers import try_to_register, try_to_login

class AuthTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_register_success(self):
        user = try_to_register(
            'bruh@bruh.com', 'bruh', 'bruh', 'bruh',
            "What was your first pet's name?", 'bruh'
        )
        self.assertIsNotNone(user)

    def test_login_success(self):
        # Register user first
        try_to_register(
            'bruhh@bruh.com', 'bruh', 'bruh', 'bruh',
            "What was your first pet's name?", 'bruh'
        )
        user = try_to_login('bruhh@bruh.com', 'bruh')
        self.assertIsNotNone(user)

    def test_login_failure(self):
        user = try_to_login('notfound@bruh.com', 'wrong')
        self.assertIsNone(user)

if __name__ == '__main__':
    unittest.main()