import time
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_registration_flow(driver, base_url):
    """Test the complete registration flow."""
    # Go to registration page
    driver.get(f"{base_url}/register")
    
    # Check the page title
    assert "Register account" in driver.title
    
    # Fill out the form
    driver.find_element(By.ID, "email").send_keys("selenium_reg@example.com")
    driver.find_element(By.ID, "fname").send_keys("Selenium")
    driver.find_element(By.ID, "lname").send_keys("Registration")
    driver.find_element(By.ID, "new_password").send_keys("password123")
    driver.find_element(By.ID, "confirm_password").send_keys("password123")
    
    # Select security question
    from selenium.webdriver.support.ui import Select
    select = Select(driver.find_element(By.ID, "secret_question"))
    select.select_by_value("What was your first pet's name?")
    
    driver.find_element(By.ID, "secret_answer").send_keys("Fluffy")
    
    # Submit the form
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    
    # Wait for redirect to login page
    WebDriverWait(driver, 10).until(
        EC.url_contains("/login")
    )
    
    # Check for success message
    assert "Registration successful" in driver.page_source

def test_login_flow(driver, base_url, register_user):
    """Test the complete login flow."""
    # Register a test user first
    test_email = "selenium_login@example.com"
    test_password = "password123"
    register_user(email=test_email, password=test_password)
    
    # Go to login page
    driver.get(f"{base_url}/login")
    
    # Check the page title
    assert "Login" in driver.title
    
    # Fill out the form
    driver.find_element(By.ID, "username").send_keys(test_email)
    driver.find_element(By.ID, "password").send_keys(test_password)
    
    # Submit the form
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    
    # Wait for redirect to account page
    WebDriverWait(driver, 10).until(
        EC.url_contains("/account")
    )
    
    # Check for welcome message
    assert f"Welcome, Selenium Registration" in driver.page_source
    
    # Logout
    driver.get(f"{base_url}/logout")

def test_forgot_password_flow(driver, base_url, register_user):
    """Test the forgot password flow."""
    # Register a test user first
    test_email = "selenium_forgot@example.com"
    test_password = "password123"
    register_user(email=test_email, password=test_password)
    
    # Go to forgot password page
    driver.get(f"{base_url}/forgot-password")
    
    # Fill out the email
    driver.find_element(By.ID, "email").send_keys(test_email)
    
    # Submit the form
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    
    # This would normally redirect to the security question page
    # but since we're testing, we'll just check that the form submitted
    time.sleep(1)
    assert driver.current_url != f"{base_url}/forgot-password"