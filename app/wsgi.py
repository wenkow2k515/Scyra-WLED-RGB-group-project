# Import using relative imports when running from inside the app directory
from . import app as flask_app

if __name__ == '__main__':
    import sys
    import os
    
    # Add the parent directory to sys.path for proper imports
    parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    sys.path.append(parent_dir)
    
    # Now import using absolute import
    from app import app
    app.run(debug=True)