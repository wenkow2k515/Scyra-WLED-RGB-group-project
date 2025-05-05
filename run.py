# This file runs the Flask application from the project root
from app import app

if __name__ == '__main__':
    app.run(debug=True, port=8888) 