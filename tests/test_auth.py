import unittest
from app import create_app, db
from app.models import User, UploadedData
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

    def test_save_and_retrieve_preset(self):
        # First, register a user
        user = try_to_register(
            'presetuser@bruh.com', 'bruh', 'Preset', 'User',
            "What was your first pet's name?", 'bruh'
        )
        self.assertIsNotNone(user)

        # Save a preset for this user
        preset = UploadedData(
            user_id=user.id,
            preset_name="Test Preset",
            preset_data={"color": "red", "pattern": "blink"},
            is_public=True
        )
        db.session.add(preset)
        db.session.commit()

        # Retrieve the preset
        loaded = UploadedData.query.filter_by(user_id=user.id, preset_name="Test Preset").first()
        self.assertIsNotNone(loaded)
        self.assertEqual(loaded.preset_data["color"], "red")
        self.assertEqual(loaded.is_public, True)

    def test_login_failure(self):
        user = try_to_login('notfound@bruh.com', 'wrong')
        self.assertIsNone(user)

if __name__ == '__main__':
    unittest.main()