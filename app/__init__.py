from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# Initialize Flask app
app = Flask(__name__)

# Configure SQLAlchemy for MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://bank:Bank#9911@localhost/bank'  # Replace with your MySQL connection string
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking (optional but recommended)
db = SQLAlchemy(app)
# Import views
from . import views

# Import models (if necessary)
from . import models

# Ensure all models are created in the database
with app.app_context():
    db.create_all()


import secrets
app.secret_key = "my_key"  # Generate a 32-character hexadecimal string (16 bytes)app.secret_key = secrets.token_hex(16)
