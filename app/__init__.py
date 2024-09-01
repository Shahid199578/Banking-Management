#__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import logging
from logging.handlers import RotatingFileHandler
import os
from itsdangerous import URLSafeSerializer
# Set a secret key for Flask
import secrets
SECRET_KEY = secrets.token_hex(16)
#FERNET_KEY = secrets.token_urlsafe(32)
import hashlib
from cryptography.fernet import Fernet

key = os.getenv('FERNET_KEY', Fernet.generate_key().decode())
cipher_suite = Fernet(key)

# Initialize Flask app
app = Flask(__name__)


# Configure SQLAlchemy for MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:Shahid@db/flask_app'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Set a secret key for Flask
app.secret_key = os.getenv('SECRET_KEY', secrets.token_hex(16))
serializer = URLSafeSerializer(app.secret_key)

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

# # Encryption functions
# def encrypt(text):
#     if isinstance(text, int):
#         text = str(text)
#     return hashlib.sha1(text.encode()).hexdigest()

<<<<<<< HEAD
# def decrypt(text):
#     return None  # SHA1 is one-way, cannot decrypt

# Encrypt account number using serializer
def encrypt(account_number):
    return cipher_suite.encrypt(str(account_number).encode()).decode()

def decrypt(encrypted_account_number):
    try:
        return cipher_suite.decrypt(encrypted_account_number.encode()).decode()
    except Exception as e:
        print(f"Decryption error: {e}")  # Log the error for debugging
        return None

=======
def decrypt(text):
    return None  # SHA1 is one-way, cannot decrypt
>>>>>>> 8ad0b0d965202959e06c4474165d2b5f64ee123b

# Import views and models
from . import views, models

# Ensure all models are created in the database
with app.app_context():
<<<<<<< HEAD
    db.create_all()
=======
    db.create_all()

# Set a secret key for Flask
import secrets
app.secret_key = secrets.token_hex(16)

>>>>>>> 8ad0b0d965202959e06c4474165d2b5f64ee123b
