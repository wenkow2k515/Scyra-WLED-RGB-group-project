from flask import Flask, url_for, render_template, request, redirect, flash, session
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, BooleanField
from wtforms.validators import DataRequired, Length, NumberRange
from werkzeug.security import generate_password_hash, check_password_hash
from .models import db, User, UploadedData, SharedData

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database with the Flask app
db.init_app(app)

# Create tables if they don't exist
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('home.html', title='Home')

@app.route('/rbg')
def rgb():
    return render_template('rgb.html', title='RGB')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['username']  # Assuming username is email
        password = request.form['password']
        
        # Look up the user in the database
        user = User.query.filter_by(email=email).first()
        
        # Check if user exists and password is correct
        if user and check_password_hash(user.password, password):
            # Set session variables
            session['user_id'] = user.id
            session['user_email'] = user.email
            session['user_fname'] = user.fname
            session['user_lname'] = user.lname
            
            flash('Login successful!', 'success')
            return redirect(url_for('account'))
        else:
            flash('Login failed. Please check your email and password.', 'error')
            return redirect(url_for('login'))
    
    # This handles GET requests
    return render_template('login.html', title='Login')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        
        # Get first name and last name from form - add these fields to your form
        fname = request.form.get('fname', '')
        lname = request.form.get('lname', '')
        email = request.form['email']  # Add this field to your registration form
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
def account():
    # Check if user is logged in
    if 'user_id' not in session:
        flash('Please log in to access this page', 'error')
        return redirect(url_for('login'))
        
    # Get user's uploaded data
    user_uploads = UploadedData.query.filter_by(user_id=session['user_id']).all()
    
    # Create user name from fname and lname
    user_name = f"{session.get('user_fname', '')} {session.get('user_lname', '')}"
    
    return render_template(
        'account.html',
        title='Account',
        user_name=user_name,
        user_email=session.get('user_email', ''),
        uploads=user_uploads
    )

@app.route('/logout')
def logout():
    # Clear the session
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run()