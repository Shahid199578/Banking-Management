from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import logging
from logging.handlers import RotatingFileHandler
import secrets
import hashlib
import os


# Initialize Flask app
app = Flask(__name__)

# Configure SQLAlchemy for MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:Shahid@db/flask_app'  # Replace with your MySQL connection string
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking (optional but recommended)
db = SQLAlchemy(app)

# Logging configuration
log_file_path = os.path.join(app.root_path, 'logs', 'app.log')
if not os.path.exists(os.path.dirname(log_file_path)):
    os.makedirs(os.path.dirname(log_file_path))

handler = RotatingFileHandler(log_file_path, maxBytes=10000, backupCount=10)
handler.setLevel(logging.ERROR)  # Log only errors and above
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

app.logger.addHandler(handler)
app.logger.setLevel(logging.ERROR)

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
