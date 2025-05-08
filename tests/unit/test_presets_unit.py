import json

def test_view_preset(client, auth, test_preset):
    """Test viewing a preset."""
    auth.login()
    response = client.get(f'/presets/{test_preset.id}/view')
    
    # Should redirect to RGB page with view mode
    assert response.status_code == 302
    assert '/rgb' in response.location
    
    # Check that session contains the preset ID and view mode
    with client.session_transaction() as sess:
        assert sess['load_preset_id'] == test_preset.id
        assert sess['view_mode'] is True

def test_edit_preset(client, auth, test_preset):
    """Test editing a preset."""
    auth.login()
    response = client.get(f'/presets/{test_preset.id}/edit')
    
    # Should redirect to RGB page with edit mode
    assert response.status_code == 302
    assert '/rgb' in response.location
    
    # Check that session contains the preset ID and edit mode
    with client.session_transaction() as sess:
        assert sess['load_preset_id'] == test_preset.id
        assert sess['edit_mode'] is True

def test_delete_preset(client, app, auth, test_preset):
    """Test deleting a preset."""
    auth.login()
    response = client.post(f'/presets/{test_preset.id}/delete')
    
    # Should redirect to account page
    assert response.status_code == 302
    assert '/account' in response.location
    
    # Check that preset was deleted
    with app.app_context():
        from app.models import UploadedData
        preset = UploadedData.query.get(test_preset.id)
        assert preset is None

def test_share_preset(client, app, auth, test_preset):
    """Test sharing a preset."""
    auth.login()
    
    # First create a user to share with
    with app.app_context():
        from app.models import db, User
        from werkzeug.security import generate_password_hash
        share_user = User(
            email='share_recip@example.com',
            password=generate_password_hash('password'),
            fname='Share',
            lname='Recipient'
        )
        db.session.add(share_user)
        db.session.commit()
    
    # Share the preset
    response = client.post(
        f'/share-preset/{test_preset.id}',
        data={'share_email': 'share_recip@example.com'},
        follow_redirects=True
    )
    
    # Check that the page contains success message
    assert b'successfully shared' in response.data
    
    # Check that the share was created in the database
    with app.app_context():
        from app.models import SharedData
        share = SharedData.query.filter_by(
            preset_id=test_preset.id,
            shared_with_id=share_user.id
        ).first()
        assert share is not None