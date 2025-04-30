from flask import Flask, url_for, render_template, request, redirect, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, BooleanField
from wtforms.validators import DataRequired, Length, NumberRange

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

@app.route('/')
def home():
    return render_template('home.html', title='Home')

@app.route('/rgb')  # Fixed route from '/rbg' to '/rgb'
def rgb():
    return render_template('rgb.html', title='RGB')

@app.route('/about')
def about():
    """Render the about page."""
    return render_template('about.html', title='About Scyra')

@app.route('/presets')
def presets():
    """Render the presets page."""
    return render_template('presets.html', title='Presets')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        print(f"Login attempt: {username}, {password}")  # Debugging output
        flash('Login functionality not implemented yet.', 'info')
        return redirect(url_for('login'))
    return render_template('login.html', title='Login')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        new_username = request.form['new_username']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']

        if new_password != confirm_password:
            flash('Passwords do not match!', 'error')
            return redirect(url_for('register'))

        # Save the new user (for now, just print it for debugging)
        print(f"New user registered: {new_username}")
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))  # Redirect to the login page

    return render_template('register.html', title='Register account')

@app.route('/account')
def account():
    return render_template('account.html', title='Account')


if __name__ == '__main__':
    app.run()