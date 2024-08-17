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
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:Shahid@db/flask_app'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Logging configuration
log_file_path = os.path.join(app.root_path, 'logs', 'app.log')
if not os.path.exists(os.path.dirname(log_file_path)):
    os.makedirs(os.path.dirname(log_file_path))

handler = RotatingFileHandler(log_file_path, maxBytes=10000, backupCount=10)
handler.setLevel(logging.ERROR)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

app.logger.addHandler(handler)
app.logger.setLevel(logging.ERROR)

# Encryption and decryption functions
def encrypt(text):
    return hashlib.sha1(text.encode()).hexdigest()

def decrypt(text):
    return None  # SHA1 is one-way, cannot decrypt

# Import views and models
from . import views, models

# Ensure all models are created in the database
with app.app_context():
    db.create_all()

# Set a secret key for Flask
import secrets
app.secret_key = secrets.token_hex(16)

