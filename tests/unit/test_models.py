from app.models import User, UploadedData, SharedData, MoodEntry, ColorSuggestion
import pytest

def test_user_creation(app):
    """Test User model creation."""
    with app.app_context():
        user = User(
            email='model@example.com',
            password='hashed_password',
            fname='Model',
            lname='Test'
        )
        assert user.email == 'model@example.com'
        assert user.password == 'hashed_password'
        assert user.fname == 'Model'
        assert user.lname == 'Test'

def test_uploaded_data_creation(app, test_user):
    """Test UploadedData model creation with proper JavaScript-compatible format."""
    with app.app_context():
        # Create preset with the structure expected by frontend
        preset_data = {
            'primary_color': 'ff0000',  # Red, without the #
            'brightness': 255,
            'cells': [
                {
                    'index': 0,
                    'color': 'rgb(255,0,0)',  # RGB format as string
                    'selected': True
                },
                {
                    'index': 1,
                    'color': 'rgb(0,255,0)',  # Green
                    'selected': False
                }
            ],
            'wled_config': {
                'segmentCount': 10,
                'segmentSize': 1,
                'totalLEDs': 10
            }
        }
        
        preset = UploadedData(
            user_id=test_user.id,
            preset_name='Model Test Preset',
            preset_data=preset_data,
            is_public=True
        )
        
        # Test basic properties
        assert preset.user_id == test_user.id
        assert preset.preset_name == 'Model Test Preset'
        assert preset.is_public is True
        
        # Test preset data structure matches expected format
        assert 'primary_color' in preset.preset_data
        assert 'brightness' in preset.preset_data
        assert 'cells' in preset.preset_data
        assert 'wled_config' in preset.preset_data
        
        # Test specific values
        assert preset.preset_data['primary_color'] == 'ff0000'
        assert preset.preset_data['brightness'] == 255
        assert len(preset.preset_data['cells']) == 2
        assert preset.preset_data['cells'][0]['color'] == 'rgb(255,0,0)'

def test_shared_data_creation(app, test_user, test_preset):
    """Test SharedData model creation."""
    with app.app_context():
        # Create second user to share with
        from werkzeug.security import generate_password_hash
        user2 = User(
            email='share@example.com',
            password=generate_password_hash('password'),
            fname='Share',
            lname='User'
        )
        from app.models import db
        db.session.add(user2)
        db.session.commit()
        
        # Create share
        share = SharedData(
            preset_id=test_preset.id,
            shared_by_id=test_user.id,
            shared_with_id=user2.id
        )
        assert share.preset_id == test_preset.id
        assert share.shared_by_id == test_user.id
        assert share.shared_with_id == user2.id