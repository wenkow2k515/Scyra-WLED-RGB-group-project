import json

def test_home_page(client):
    """Test that the home page loads correctly."""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Scyra' in response.data

def test_about_page(client):
    """Test that the about page loads correctly."""
    response = client.get('/about')
    assert response.status_code == 200
    assert b'About Scyra' in response.data

def test_rgb_page(client):
    """Test that the RGB page loads correctly."""
    response = client.get('/rgb')
    assert response.status_code == 200
    assert b'Build Your Preset' in response.data

def test_presets_page(client):
    """Test that the presets page loads correctly."""
    response = client.get('/presets')
    assert response.status_code == 200
    assert b'Your Light Presets' in response.data

def test_login_required_account(client):
    """Test that the account page redirects when not logged in."""
    response = client.get('/account')
    # Should redirect to login page
    assert response.status_code == 302
    assert '/login' in response.location

def test_account_page_when_logged_in(client, auth, test_user):
    """Test that the account page loads when logged in."""
    auth.login()  # Log in the test user
    response = client.get('/account')
    assert response.status_code == 200
    assert b'Your Saved Presets' in response.data
    assert b'Welcome, Test User' in response.data

def test_save_preset(client, auth, test_user):
    """Test saving a preset."""
    auth.login()  # Log in the test user
    
    preset_data = {
        'preset_name': 'Test Preset',
        'preset_data': {'leds': [{'color': [255, 0, 0]}, {'color': [0, 255, 0]}]},
        'is_public': True
    }
    
    response = client.post(
        '/save-preset',
        json=preset_data,
        content_type='application/json'
    )
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] is True
    assert 'preset_id' in data