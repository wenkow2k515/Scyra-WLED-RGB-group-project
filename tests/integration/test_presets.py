import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_presets_page_loads(driver, base_url):
    """Test that the presets page loads correctly."""
    driver.get(f"{base_url}/presets")
    
    # Check for the presets container
    presets_container = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "presets-container"))
    )
    assert presets_container.is_displayed()
    
    # Check that tabs are present
    tabs = driver.find_elements(By.CLASS_NAME, "tab-btn")
    assert len(tabs) == 3
    assert "Local Presets" in tabs[0].text
    assert "Cloud Presets" in tabs[1].text
    assert "Community Presets" in tabs[2].text

def test_switch_preset_tabs(driver, base_url):
    """Test switching between preset tabs."""
    driver.get(f"{base_url}/presets")
    
    # Click on Cloud Presets tab
    cloud_tab = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".tab-btn[data-tab='cloud']"))
    )
    cloud_tab.click()
    
    # Check that the cloud presets tab content is visible
    cloud_content = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "cloud-presets"))
    )
    assert cloud_content.is_displayed()
    
    # Click on Community Presets tab
    community_tab = driver.find_element(By.CSS_SELECTOR, ".tab-btn[data-tab='community']")
    community_tab.click()
    
    # Check that the community presets tab content is visible
    community_content = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "community-presets"))
    )
    assert community_content.is_displayed()

def test_view_preset_button(driver, base_url, login_user):
    """Test viewing a preset."""
    # Login first to ensure we have access to presets
    login_user()
    
    # Create a test preset (this would require integration with your app)
    # For this test, we'll assume a preset exists in the community tab
    
    # Go to presets page
    driver.get(f"{base_url}/presets")
    
    # Click on Community Presets tab
    community_tab = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".tab-btn[data-tab='community']"))
    )
    community_tab.click()
    
    # Check if there are any preset cards
    preset_cards = driver.find_elements(By.CLASS_NAME, "preset-card")
    if preset_cards:
        # Find a view button and click it
        view_buttons = driver.find_elements(By.CLASS_NAME, "view-preset")
        if view_buttons:
            view_buttons[0].click()
            
            # Check that we're redirected to the RGB page with view mode
            time.sleep(2)
            assert "/rgb" in driver.current_url
            
            # We'd expect the preset to be loaded in view mode
            # This would require additional verification specific to your app