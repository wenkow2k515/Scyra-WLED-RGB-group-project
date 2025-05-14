from flask import Flask, url_for, render_template, request, redirect, flash, session, jsonify
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate
from wtforms import StringField, SubmitField, IntegerField, BooleanField
from wtforms.validators import DataRequired, Length, NumberRange
from werkzeug.security import generate_password_hash, check_password_hash
import os

from app.config import config
from app.models import db, User, UploadedData, SharedData

# Create a function to create the app with the specified configuration
def create_app(config_name='testing'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    migrate = Migrate(app, db)  # Initialize Flask-Migrate
    
    # Initialize CSRF protection
    csrf = CSRFProtect(app)
    
    # Initialize Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'core.login'
    login_manager.login_message = 'Please log in to access this page'
    login_manager.login_message_category = 'error'
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Register routes
    # (Your routes would go here...)
    
    # Register blueprints
    with app.app_context():
        # Import and register blueprints inside app context
        try:
            from app.mood_routes import mood
            app.register_blueprint(mood)
            print("Mood blueprint registered successfully.")
        except ImportError as e:
            print(f"Mood blueprint could not be imported - will be skipped. Error: {e}")

        try:
            from app.routes import core  # Import the core blueprint
            app.register_blueprint(core)  # Register the core blueprint
            print("Core blueprint registered successfully.")
        except ImportError as e:
            print(f"Core blueprint could not be imported - will be skipped. Error: {e}")
    
    return app