import os

# Get the base directory
basedir = os.path.abspath(os.path.dirname(__file__))

# Create database directory path
database_dir = os.path.join(basedir, 'database')

# Create the directory if it doesn't exist
os.makedirs(database_dir, exist_ok=True)

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'default-key-for-dev'  # Better: os.environ.get('SECRET_KEY') or 'fallback_key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(database_dir, 'site.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # Use in-memory database for tests
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False  # Disable CSRF for testing

# Dictionary to easily access different configurations
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}