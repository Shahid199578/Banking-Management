from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import secrets
import hashlib


# Initialize Flask app
app = Flask(__name__)

# Configure SQLAlchemy for MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:Shahid@db/flask_app'  # Replace with your MySQL connection string
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking (optional but recommended)
db = SQLAlchemy(app)

# Encryption and decryption functions
def encrypt(text):
    return hashlib.sha1(text.encode()).hexdigest()

def decrypt(text):
    # Since SHA1 is a one-way hash function, decryption is not possible
    # You can consider using a different encryption algorithm if decryption is needed
    return None


# Import views and models
from . import views, models


# Ensure all models are created in the database
with app.app_context():
    db.create_all()


import secrets
app.secret_key = secrets.token_hex(16)
