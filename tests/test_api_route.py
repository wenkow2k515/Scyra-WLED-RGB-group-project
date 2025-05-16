import pytest
from flask import jsonify
from app import create_app
from app.mood_utils import generate_feedback_and_color

@pytest.fixture
def app():
    """Create and configure a Flask app for testing."""
    app = create_app('testing')
    return app

@pytest.fixture
def client(app):
    """Create a test client for the app."""
    return app.test_client()

def test_api_endpoint_with_valid_data(client):
    """Test the API endpoint with valid data."""
    test_data = {
        "energy": "7",
        "happiness": "8",
        "stress": "3",
        "anxiety": "2",
        "creativity": "6",
        "relax": "yes",
        "focus": "no",
        "journal": "Feeling great today!"
    }
    
    response = client.post('/mood/api/analyze', json=test_data)
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert 'feedback' in data
    assert 'color_name' in data
    assert 'rgb_values' in data
    assert 'hex_color' in data

def test_api_endpoint_with_missing_data(client):
    """Test the API endpoint with missing data."""
    test_data = {
        "energy": "5",
        "happiness": "5"
        # Missing other fields
    }
    
    response = client.post('/mood/api/analyze', json=test_data)
    assert response.status_code == 200  # Should still work with default values
    data = response.get_json()
    assert data['success'] is True

def test_api_endpoint_with_invalid_data(client):
    """Test the API endpoint with invalid data."""
    test_data = {
        "energy": "invalid",
        "happiness": "invalid",
        "stress": "invalid",
        "anxiety": "invalid",
        "creativity": "invalid",
        "relax": "invalid",
        "focus": "invalid",
        "journal": 123  # Invalid type
    }
    
    response = client.post('/mood/api/analyze', json=test_data)
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, dict)

def test_api_endpoint_with_empty_data(client):
    """Test the API endpoint with empty data."""
    response = client.post('/mood/api/analyze', json={})
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True 