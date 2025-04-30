import os

# Get the base directory
basedir = os.path.abspath(os.path.dirname(__file__))

# Create database directory path
database_dir = os.path.join(basedir, 'database')

# Create the directory if it doesn't exist
os.makedirs(database_dir, exist_ok=True)

class Config:
    SECRET_KEY = 'your_secret_key'  # Better: os.environ.get('SECRET_KEY') or 'fallback_key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(database_dir, 'site.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'test.db')
    WTF_CSRF_ENABLED = False

# Dictionary to easily access different configurations
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}