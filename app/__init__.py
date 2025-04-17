from flask import Flask, url_for, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, BooleanField
from wtforms.validators import DataRequired, Length, NumberRange
import app.routes

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

@app.route('/')
def home():
    return render_template('home.html', title='Home')

@app.route('/login')
def login():
    return render_template('login.html', title='Login')

@app.route('/register')
def register():
    return render_template('register.html', title='Register')


if __name__ == '__main__':
    app.run()