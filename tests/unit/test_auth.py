import re
from flask import session

def test_register(client, app):
    """Test registration functionality."""
    response = client.post('/register', data={
        'email': 'new@example.com',
        'new_password': 'password',
        'confirm_password': 'password',
        'fname': 'New',
        'lname': 'User',
        'secret_question': 'What is your favorite color?',
        'secret_answer': 'red'
    })
    
    # Should redirect to login page
    assert response.status_code == 302
    assert '/login' in response.location
    
    # Verify the user was created in the database
    with app.app_context():
        from app.models import User
        user = User.query.filter_by(email='new@example.com').first()
        assert user is not None
        assert user.fname == 'New'
        assert user.lname == 'User'
        from werkzeug.security import check_password_hash
        assert check_password_hash(user.password, 'password')

def test_login(client, auth, test_user):
    """Test login functionality."""
    response = auth.login()
    
    # Should redirect to account page
    assert response.status_code == 302
    assert '/account' in response.location
    
    # Check that the user is logged in (session contains user_id)
    with client.session_transaction() as sess:
        assert '_user_id' in sess
        assert int(sess['_user_id']) == test_user.id

def test_login_invalid_credentials(client):
    """Test login with invalid credentials."""
    response = client.post(
        '/login',
        data={'username': 'wrong@example.com', 'password': 'wrong'}
    )
    
    # Should stay on login page
    assert response.status_code == 302
    assert '/login' in response.location
    
    # Check flash message
    response = client.get('/login')  # Follow redirect
    assert b'Login failed' in response.data

def test_logout(client, auth):
    """Test logout functionality."""
    auth.login()
    response = auth.logout()
    
    # Should redirect to login page
    assert response.status_code == 302
    assert '/login' in response.location
    
    # Check that the user is logged out (session doesn't contain user_id)
    with client.session_transaction() as sess:
        assert '_user_id' not in sess