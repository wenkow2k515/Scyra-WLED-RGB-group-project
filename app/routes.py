from flask import Flask, url_for, render_template, request, redirect, flash, session, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from . import app
from .models import db, User, UploadedData, SharedData

@app.route('/')
def home():
    return render_template('home.html', title='Home')

@app.route('/rgb')
def rgb():
    """Render the RGB control page."""
    # Check if there's a preset to load from session
    preset_data = None
    preset_name = None
    preset_id = session.pop('load_preset_id', None)
    view_mode = session.pop('view_mode', False)
    edit_mode = session.pop('edit_mode', False)
    
    if preset_id:
        # Get the preset from database
        preset = UploadedData.query.get(preset_id)
        if preset:
            # Make sure we're sending the full preset data
            preset_data = preset.preset_data
            preset_name = preset.preset_name
    
    return render_template(
        'rgb.html', 
        title='RGB Editor',
        preset_data=preset_data,
        preset_name=preset_name,
        preset_id=preset_id,
        view_mode=view_mode,
        edit_mode=edit_mode
    )

@app.route('/login', methods=['GET', 'POST'])
def login():
    # If user is already logged in, redirect to account page
    if current_user.is_authenticated:
        return redirect(url_for('account'))
        
    if request.method == 'POST':
        email = request.form['username']  # Assuming username is email
        password = request.form['password']
        remember = 'remember' in request.form  # Check if "remember me" was checked
        
        # Look up the user in the database
        user = User.query.filter_by(email=email).first()
        
        # Check if user exists and password is correct
        if user and check_password_hash(user.password, password):
            # Log in the user with Flask-Login
            login_user(user, remember=remember)
            
            # Check if user was redirected to login from another page
            next_page = request.args.get('next')
            
            flash('Login successful!', 'success')
            return redirect(next_page or url_for('account'))
        else:
            flash('Login failed. Please check your email and password.', 'error')
            return redirect(url_for('login'))
    
    # This handles GET requests
    return render_template('login.html', title='Login')

@app.route('/register', methods=['GET', 'POST'])
def register():
    # If user is already logged in, redirect to account page
    if current_user.is_authenticated:
        return redirect(url_for('account'))
        
    if request.method == 'POST':
        # Get first name and last name from form
        fname = request.form.get('fname', '')
        lname = request.form.get('lname', '')
        email = request.form['email']
        # Get password and confirm password from form
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']

        # Check if passwords match
        if new_password != confirm_password:
            flash('Passwords do not match!', 'error')
            return redirect(url_for('register'))

        # Check if user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already registered!', 'error')
            return redirect(url_for('register'))

        # Create new user
        hashed_password = generate_password_hash(new_password)
        new_user = User(
            fname=fname,
            lname=lname,
            password=hashed_password,
            email=email
        )
        
        # Add user to database
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', title='Register account')

@app.route('/account')
@login_required  # Protect this route - user must be logged in
def account():
    # Get user's uploaded data
    user_uploads = UploadedData.query.filter_by(user_id=current_user.id).all()
    
    # Create user name from fname and lname
    user_name = f"{current_user.fname} {current_user.lname}"
    
    return render_template(
        'account.html',
        title='Account',
        user_name=user_name,
        user_email=current_user.email,
        uploads=user_uploads
    )

@app.route('/logout')
@login_required  # Only logged-in users can log out
def logout():
    logout_user()  # Use Flask-Login's logout function
    flash('You have been logged out', 'info')
    return redirect(url_for('login'))

@app.route('/about')
def about():
    """Render the about page."""
    return render_template('about.html', title='About Scyra')

@app.route('/presets')
def presets():
    """Render the presets page with presets from the database."""
    # Get all public presets
    public_presets = UploadedData.query.filter_by(is_public=True).all()
    
    # Get presets shared with current user
    shared_presets = []
    if current_user.is_authenticated:
        # Find all presets shared with the current user
        shared_data = SharedData.query.filter_by(shared_with_id=current_user.id).all()
        # Make sure the relationship works correctly
        shared_presets = []
        for data in shared_data:
            preset = UploadedData.query.get(data.preset_id)
            if preset:
                shared_presets.append(preset)
    
    # Get user's private presets
    user_presets = []
    if current_user.is_authenticated:
        user_presets = UploadedData.query.filter_by(user_id=current_user.id).all()
    
    return render_template(
        'presets.html', 
        title='Presets',
        public_presets=public_presets,
        user_presets=user_presets,
        shared_presets=shared_presets
    )

@app.route('/save-preset', methods=['POST'])
@login_required
def save_preset():
    """Save preset to user account."""
    if not request.is_json:
        return jsonify({'success': False, 'error': 'Invalid request format'})
    
    data = request.get_json()
    
    preset_name = data.get('preset_name')
    preset_data = data.get('preset_data')
    is_public = data.get('is_public', False)
    preset_id = data.get('preset_id')  # Used in edit mode
    
    if not preset_name or not preset_data:
        return jsonify({'success': False, 'error': 'Missing required fields'})
    
    try:
        # Check if updating an existing preset
        if preset_id:
            existing_preset = UploadedData.query.get(preset_id)
            # Verify ownership
            if existing_preset and existing_preset.user_id == current_user.id:
                existing_preset.preset_name = preset_name
                existing_preset.preset_data = preset_data
                existing_preset.is_public = is_public
                db.session.commit()
                return jsonify({
                    'success': True, 
                    'message': 'Preset successfully updated',
                    'preset_id': existing_preset.id
                })
            else:
                return jsonify({'success': False, 'error': 'You do not have permission to edit this preset'})
        
        # Check if user already has a preset with the same name
        existing_preset = UploadedData.query.filter_by(
            user_id=current_user.id, 
            preset_name=preset_name
        ).first()
        
        if existing_preset:
            existing_preset.preset_data = preset_data
            existing_preset.is_public = is_public
            db.session.commit()
            return jsonify({
                'success': True, 
                'message': 'Preset successfully updated',
                'preset_id': existing_preset.id
            })
        else:
            # Create a new preset
            new_preset = UploadedData(
                user_id=current_user.id,
                preset_name=preset_name,
                preset_data=preset_data,
                is_public=is_public
            )
            db.session.add(new_preset)
            db.session.commit()
            return jsonify({
                'success': True, 
                'message': 'Preset successfully saved',
                'preset_id': new_preset.id
            })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)})

@app.route('/presets/<int:preset_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_preset(preset_id):
    """Delete preset."""
    # Get preset
    preset = UploadedData.query.get_or_404(preset_id)
    
    # Verify ownership
    if preset.user_id != current_user.id:
        flash('You do not have permission to delete this preset', 'error')
        return redirect(url_for('account'))
    
    try:
        # First delete related shared data
        SharedData.query.filter_by(preset_id=preset_id).delete()
        
        # Delete preset
        db.session.delete(preset)
        db.session.commit()
        flash('Preset successfully deleted', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Deletion failed: {str(e)}', 'error')
    
    return redirect(url_for('account'))

@app.route('/share-preset/<int:preset_id>', methods=['GET', 'POST'])
@login_required
def share_preset(preset_id):
    """Share preset with other users."""
    # Get preset
    preset = UploadedData.query.get_or_404(preset_id)
    
    # Verify ownership
    if preset.user_id != current_user.id:
        flash('You do not have permission to share this preset', 'error')
        return redirect(url_for('account'))
    
    if request.method == 'POST':
        # Get the email of the user to share with
        share_email = request.form.get('share_email')
        
        if not share_email:
            flash('Please enter a valid email address', 'error')
            return redirect(url_for('share_preset', preset_id=preset_id))
        
        # Find user
        user = User.query.filter_by(email=share_email).first()
        if not user:
            flash('User not found', 'error')
            return redirect(url_for('share_preset', preset_id=preset_id))
        
        # Ensure it's not the current user
        if user.id == current_user.id:
            flash('You cannot share a preset with yourself', 'error')
            return redirect(url_for('share_preset', preset_id=preset_id))
        
        # Check if already shared
        existing_share = SharedData.query.filter_by(
            preset_id=preset_id,
            shared_with_id=user.id
        ).first()
        
        if existing_share:
            flash('This preset is already shared with the user', 'info')
            return redirect(url_for('share_preset', preset_id=preset_id))
        
        # Create a new share
        new_share = SharedData(
            preset_id=preset_id,
            shared_by_id=current_user.id,
            shared_with_id=user.id
        )
        db.session.add(new_share)
        db.session.commit()
        
        flash(f'Preset successfully shared with {user.email}', 'success')
        return redirect(url_for('account'))
    
    # GET request - show share form
    return render_template(
        'share_preset.html',
        title='Share Preset',
        preset=preset
    )

@app.route('/unshare-preset/<int:share_id>', methods=['POST'])
@login_required
def unshare_preset(share_id):
    """Unshare preset with a user."""
    # Get share record
    shared_data = SharedData.query.get_or_404(share_id)
    preset_id = shared_data.preset_id
    
    # Verify ownership
    preset = UploadedData.query.get(preset_id)
    if not preset or preset.user_id != current_user.id:
        flash('You do not have permission to modify this share', 'error')
        return redirect(url_for('account'))
    
    # Delete share
    db.session.delete(shared_data)
    db.session.commit()
    
    flash('Share successfully removed', 'success')
    return redirect(url_for('share_preset', preset_id=preset_id))

@app.route('/presets/<int:preset_id>/view')
def view_preset(preset_id):
    """View preset (read-only mode)."""
    # Get preset
    preset = UploadedData.query.get_or_404(preset_id)
    
    # Check permissions
    has_access = False
    
    # Preset is public
    if preset.is_public:
        has_access = True
    # User is logged in
    elif current_user.is_authenticated:
        # User is the owner of the preset
        if preset.user_id == current_user.id:
            has_access = True
        # Preset is shared with the user
        else:
            shared = SharedData.query.filter_by(
                preset_id=preset_id, 
                shared_with_id=current_user.id
            ).first()
            has_access = shared is not None
    
    if not has_access:
        flash('You do not have permission to view this preset', 'error')
        return redirect(url_for('presets'))
    
    # Set view_mode to True and pass preset data
    session['load_preset_id'] = preset_id
    session['view_mode'] = True

    return redirect(url_for('rgb'))

@app.route('/presets/<int:preset_id>/edit')
@login_required
def edit_preset(preset_id):
    """Edit an existing preset."""
    # Get preset
    preset = UploadedData.query.get_or_404(preset_id)
    
    # Verify ownership
    if preset.user_id != current_user.id:
        flash('You do not have permission to edit this preset', 'error')
        return redirect(url_for('account'))
    
    # Store preset ID in session for RGB editor to load
    session['load_preset_id'] = preset_id
    session['edit_mode'] = True
    
    # Redirect to RGB editor
    return redirect(url_for('rgb'))

@app.route('/presets/<int:preset_id>/load')
def load_preset(preset_id):
    """Load preset into RGB editor."""
    # Get preset
    preset = UploadedData.query.get_or_404(preset_id)
    
    # Check permissions (same as view_preset)
    has_access = False
    
    if preset.is_public:
        has_access = True
    elif current_user.is_authenticated:
        if preset.user_id == current_user.id:
            has_access = True
        else:
            shared = SharedData.query.filter_by(
                preset_id=preset_id, 
                shared_with_id=current_user.id if current_user.is_authenticated else None
            ).first()
            has_access = shared is not None
    
    if not has_access:
        flash('You do not have permission to load this preset', 'error')
        return redirect(url_for('presets'))
    
    # Store preset ID in session for RGB editor to load
    session['load_preset_id'] = preset_id
    
    # Redirect to RGB editor
    return redirect(url_for('rgb'))

if __name__ == '__main__':
    app.run()