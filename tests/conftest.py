import pytest
import time
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager

@pytest.fixture(scope="session")
def driver():
    """Set up WebDriver instance for Firefox."""
    firefox_options = Options()
    firefox_options.add_argument("--headless")  # Run in headless mode
    firefox_options.add_argument("--no-sandbox")
    firefox_options.add_argument("--disable-dev-shm-usage")
    firefox_options.add_argument("--width=1920")
    firefox_options.add_argument("--height=1080")
    
    driver = webdriver.Firefox(
        service=Service(GeckoDriverManager().install()),
        options=firefox_options
    )
    driver.implicitly_wait(10)  # Wait up to 10 seconds for elements
    
    yield driver
    
    # Quit the driver after tests
    driver.quit()

@pytest.fixture(scope="session")
def base_url():
    """Return the base URL for the application."""
    return "http://localhost:5000"

@pytest.fixture
def register_user(driver, base_url):
    """Helper to register a test user."""
    def _register(email="selenium@example.com", password="password", fname="Selenium", lname="Test"):
        driver.get(f"{base_url}/register")
        
        # Fill out registration form
        driver.find_element("id", "email").send_keys(email)
        driver.find_element("id", "fname").send_keys(fname)
        driver.find_element("id", "lname").send_keys(lname)
        driver.find_element("id", "new_password").send_keys(password)
        driver.find_element("id", "confirm_password").send_keys(password)
        
        # Select a security question
        from selenium.webdriver.support.select import Select
        select = Select(driver.find_element("id", "secret_question"))
        select.select_by_index(1)  # Select the second option
        
        driver.find_element("id", "secret_answer").send_keys("answer")
        
        # Submit the form
        driver.find_element("tag name", "button").click()
        
        # Wait for redirect
        time.sleep(1)
        
    return _register

@pytest.fixture
def login_user(driver, base_url):
    """Helper to log in a test user."""
    def _login(email="selenium@example.com", password="password"):
        driver.get(f"{base_url}/login")
        
        # Fill out login form
        driver.find_element("id", "username").send_keys(email)
        driver.find_element("id", "password").send_keys(password)
        
        # Submit the form
        driver.find_element("tag name", "button").click()
        
        # Wait for redirect
        time.sleep(1)
        
    return _login

@pytest.fixture
def logout_user(driver, base_url):
    """Helper to log out."""
    def _logout():
        driver.get(f"{base_url}/logout")
        # Wait for redirect
        time.sleep(1)
        
    return _logout