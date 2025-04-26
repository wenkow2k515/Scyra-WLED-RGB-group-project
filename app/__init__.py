from flask import Flask, url_for, render_template, request, redirect, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, BooleanField
from wtforms.validators import DataRequired, Length, NumberRange

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

@app.route('/')
def home():
    return render_template('home.html', title='Home')

@app.route('/step1_2', methods=['GET', 'POST'])
def step1_2():
    if request.method == 'POST':
        # Get inputs from step 1 and step 2
        wled_address = request.form['wledAddress']
        group_size = request.form['groupSize']

        # Validate inputs
        if not wled_address or not group_size.isdigit() or int(group_size) <= 0:
            flash('Invalid input. Please check your WLED address and group size.', 'error')
            return redirect(url_for('step1_2'))

        # Pass the data to step 3
        return redirect(url_for('step3', wled_address=wled_address, group_size=group_size))

    return render_template('step1_2.html', title='Step 1 & 2')

@app.route('/step3')
def step3():
    # Get data passed from step 1 and 2
    wled_address = request.args.get('wled_address')
    group_size = request.args.get('group_size')

    if not wled_address or not group_size:
        flash('Missing data from step 1 or 2.', 'error')
        return redirect(url_for('step1_2'))

    return render_template('rgb.html', title='Step 3', wled_address=wled_address, group_size=group_size)


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