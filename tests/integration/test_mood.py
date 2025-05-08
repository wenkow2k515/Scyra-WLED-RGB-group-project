import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

def test_mood_page_loads(driver, base_url, login_user):
    """Test that the mood page loads correctly."""
    # Login first since mood page requires authentication
    login_user()
    
    # Go to mood page
    driver.get(f"{base_url}/mood")
    
    # Check that the mood dashboard is displayed
    dashboard = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "mood-dashboard"))
    )
    assert dashboard.is_displayed()
    
    # Check for the survey button
    survey_btn = driver.find_element(By.LINK_TEXT, "Take Survey")
    assert survey_btn.is_displayed()

def test_mood_survey_workflow(driver, base_url, login_user):
    """Test taking a mood survey."""
    # Login first
    login_user()
    
    # Go to mood survey page
    driver.get(f"{base_url}/mood/survey")
    
    # Check that the survey form is displayed
    survey_form = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "form"))
    )
    assert survey_form.is_displayed()
    
    # Set energy level (range input requires JavaScript)
    energy_slider = driver.find_element(By.ID, "energy_level")
    driver.execute_script("arguments[0].value = 8;", energy_slider)
    driver.execute_script("arguments[0].dispatchEvent(new Event('change'));", energy_slider)
    
    # Set happiness level
    happiness_slider = driver.find_element(By.ID, "happiness")
    driver.execute_script("arguments[0].value = 9;", happiness_slider)
    driver.execute_script("arguments[0].dispatchEvent(new Event('change'));", happiness_slider)
    
    # Set anxiety level
    anxiety_slider = driver.find_element(By.ID, "anxiety")
    driver.execute_script("arguments[0].value = 3;", anxiety_slider)
    driver.execute_script("arguments[0].dispatchEvent(new Event('change'));", anxiety_slider)
    
    # Set stress level
    stress_slider = driver.find_element(By.ID, "stress")
    driver.execute_script("arguments[0].value = 2;", stress_slider)
    driver.execute_script("arguments[0].dispatchEvent(new Event('change'));", stress_slider)
    
    # Add some notes
    notes_input = driver.find_element(By.ID, "notes")
    notes_input.send_keys("Feeling great today!")
    
    # Submit the form
    submit_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    submit_btn.click()
    
    # Check that we're redirected to the results page
    WebDriverWait(driver, 10).until(
        EC.url_contains("/results")
    )
    
    # Check that the results page contains color suggestions
    assert "Color Suggestion" in driver.page_source