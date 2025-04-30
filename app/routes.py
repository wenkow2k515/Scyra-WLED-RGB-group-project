from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from . import app
from .models import db, User, UploadedData, SharedData

@app.route('/')
def home():
    return render_template('home.html', title='Home')

@app.route('/rbg')
def rgb():
    return render_template('rgb.html', title='RGB')

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


if __name__ == '__main__':
    app.run()