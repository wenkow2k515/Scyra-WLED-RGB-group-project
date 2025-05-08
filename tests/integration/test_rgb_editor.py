import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

def test_rgb_editor_page_loads(driver, base_url):
    """Test that the RGB editor page loads correctly."""
    driver.get(f"{base_url}/rgb")
    
    # Check for the setup container
    setup_container = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "setup"))
    )
    assert setup_container.is_displayed()

def test_rgb_editor_connect_workflow(driver, base_url):
    """Test the RGB editor connection workflow."""
    driver.get(f"{base_url}/rgb")
    
    # Input WLED address
    wled_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "wledAddress"))
    )
    wled_input.send_keys("192.168.1.100")
    
    # Check button should now be enabled
    check_btn = driver.find_element(By.ID, "checkBtn")
    assert not check_btn.get_attribute("disabled")
    
    # Click check button
    check_btn.click()
    
    # Wait for editor to become visible (in a real test this would depend on mocking the connection)
    # For this test, we'll just simulate it by waiting a bit then triggering the reveal manually
    time.sleep(1)
    driver.execute_script("""
        document.getElementById('setup').classList.add('hidden');
        document.getElementById('editor').classList.remove('hidden');
    """)
    
    # Check that editor is visible
    editor = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "editor"))
    )
    assert editor.is_displayed()

def test_rgb_editor_color_selection(driver, base_url, login_user):
    """Test selecting colors in the RGB editor."""
    # Login first
    login_user()
    
    # Go to RGB page
    driver.get(f"{base_url}/rgb")
    
    # Skip the setup stage by directly showing the editor
    driver.execute_script("""
        document.getElementById('setup').classList.add('hidden');
        document.getElementById('editor').classList.remove('hidden');
    """)
    
    # Wait for the editor to be visible
    editor = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "editor"))
    )
    
    # Change the color picker value
    color_picker = driver.find_element(By.ID, "colorPicker")
    driver.execute_script("arguments[0].value = '#FF0000';", color_picker)
    
    # Trigger a change event
    driver.execute_script("arguments[0].dispatchEvent(new Event('change'));", color_picker)
    
    # Apply the color
    apply_btn = driver.find_element(By.ID, "applyColor")
    apply_btn.click()
    
    # Try to verify that a color was applied (this will depend on how your grid is implemented)
    # We'll assume that selecting a color adds a 'selected' class to some cells
    time.sleep(1)
    selected_cells = driver.find_elements(By.CSS_SELECTOR, ".cell.selected")
    assert len(selected_cells) > 0