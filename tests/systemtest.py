import multiprocessing
import unittest
from app import create_app, db
from app.models import User
from tests.controllers import try_to_register, try_to_login
import threading
import os
import signal

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import time
from werkzeug.security import generate_password_hash

class SystemAuthTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Create the Flask app once for all tests
        cls.app = create_app('testing')
        cls.app_context = cls.app.app_context()
        cls.app_context.push()
        db.create_all()

        # Start the Flask server in a separate thread
        cls.server_thread = threading.Thread(target=cls.app.run, kwargs={'port': 5000})
        cls.server_thread.daemon = True
        cls.server_thread.start()
        time.sleep(1)  # Give the server time to start

    def setUp(self):
        # Create a new browser instance for each test
        options = webdriver.FirefoxOptions()
        options.add_argument('--headless')
        self.driver = webdriver.Firefox(options=options)

    def tearDown(self):
        self.driver.quit()
        # Clean up the database after each test
        db.session.remove()
        db.drop_all()
        db.create_all()

    @classmethod
    def tearDownClass(cls):
        # Clean up the Flask app and server
        cls.app_context.pop()
        # The daemon thread will be killed automatically when the main program exits

    def test_register_page(self):
        self.driver.get('http://localhost:5000/register')
        self.assertIn("Register", self.driver.title)

        # Fill in the registration form using the correct field IDs or names
        self.driver.find_element(By.ID, 'email').send_keys('selenium@bruh.com')
        self.driver.find_element(By.ID, 'password').send_keys('bruh')
        self.driver.find_element(By.ID, 'confirm_password').send_keys('bruh')
        self.driver.find_element(By.ID, 'fname').send_keys('bruh')
        self.driver.find_element(By.ID, 'lname').send_keys('bruh')
        self.driver.find_element(By.ID, 'secret_question').send_keys("What was your first pet's name?")
        self.driver.find_element(By.ID, 'secret_answer').send_keys('bruh')

        # Submit the form (adjust selector if your button is different)
        self.driver.find_element(By.CSS_SELECTOR, 'form button[type=submit]').click()


        time.sleep(10)  # For demonstration; use WebDriverWait for production

        # Assert that registration was successful (look for a flash message or redirect)
        self.assertIn("login", self.driver.current_url)  # Redirects to login page

    def test_login_page(self):
        # First, register the user directly in the DB (so you can log in via the UI)
        try_to_register(
            'selenium_login@bruh.com', 'bruh', 'bruh', 'bruh',
            "What was your first pet's name?", 'bruh'
        )

        self.driver.get('http://localhost:5000/login')
        self.assertIn("Sign In", self.driver.page_source)  # Check page loaded

        # Fill in the login form using the correct field IDs or names
        self.driver.find_element(By.ID, 'email').send_keys('selenium_login@bruh.com')
        self.driver.find_element(By.ID, 'password').send_keys('bruh')

        # Submit the form (adjust selector if your button is different)
        self.driver.find_element(By.ID, 'submit').click()

        # Wait for redirect or page update
        time.sleep(2)  # For demonstration; use WebDriverWait for production

        # Assert that login was successful (look for account page or flash message)
        self.assertIn("Account", self.driver.page_source)  # Or check for a unique element on the account page

    def test_login_failure(self):
        self.driver.get('http://localhost:5000/login')
        self.assertIn("Sign In", self.driver.page_source)  # Check page loaded

        # Fill in the login form with invalid credentials
        self.driver.find_element(By.ID, 'email').send_keys('notfound@bruh.com')
        self.driver.find_element(By.ID, 'password').send_keys('wrong')

        # Submit the form
        self.driver.find_element(By.ID, 'submit').click()

        # Wait for page update
        time.sleep(2)  # For demonstration; use WebDriverWait for production

        # Assert that login failed (look for error message or that login page is still shown)
        self.assertIn("Sign In", self.driver.page_source)  # Still on login page
        # Optionally, check for a specific error message:
        # self.assertIn("Login unsuccessful", self.driver.page_source)

    def test_dashboard_access_after_login(self):
        # Register a user directly in the DB
        try_to_register(
            'dashboard_test@bruh.com', 'bruh', 'bruh', 'bruh',
            "What was your first pet's name?", 'bruh'
        )

        # Login through the UI
        self.driver.get('http://localhost:5000/login')
        self.driver.find_element(By.ID, 'email').send_keys('dashboard_test@bruh.com')
        self.driver.find_element(By.ID, 'password').send_keys('bruh')
        self.driver.find_element(By.ID, 'submit').click()

        # Wait for login to complete
        time.sleep(2)

        # Navigate to account page
        self.driver.get('http://localhost:5000/account')
        
        # Assert that we can access the account page
        self.assertIn("Account", self.driver.page_source)

if __name__ == '__main__':
    unittest.main()