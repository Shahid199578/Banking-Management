import os
import sys

# Add the directory containing your project (the parent directory of the 'app' package) to the sys.path
project_dir = '/var/www/html/flask_app/'
if project_dir not in sys.path:
    sys.path.append(project_dir)

# Import the Flask app instance
from app import app as application
