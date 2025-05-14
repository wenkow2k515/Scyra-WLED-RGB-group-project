import multiprocessing
import unittest
from app import create_app, db
from app.models import User
from tests.controllers import try_to_register, try_to_login

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import time

class SystemAuthTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        self.server_thread = multiprocessing.Process(target=self.app.run, kwargs={'port': 5000})
        self.server_thread.start()

        options = webdriver.FirefoxOptions()
        options.add_argument('--headless')  # Run in headless mode
        self.driver = webdriver.Firefox()  # You can use any other driver you prefer

        return super().setUp()

    def tearDown(self):
        self.driver.quit()  # <-- This closes the browser window
        self.server_thread.terminate()
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

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

if __name__ == '__main__':
    unittest.main()