from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import mysql.connector
from mysql.connector import Error
import logging
from logging.handlers import RotatingFileHandler
import secrets
import hashlib
import os

def create_database_if_not_exists():
    try:
        # Connect to the RDS instance
        connection = mysql.connector.connect(
            host=os.getenv('RDS_HOST'),
            user=os.getenv('RDS_USER'),
            password=os.getenv('RDS_PASSWORD')
        )

        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {os.getenv('RDS_DATABASE')}")
            print(f"Database '{os.getenv('RDS_DATABASE')}' created or already exists.")

    except Error as e:
        print(f"Error: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Initialize Flask app
app = Flask(__name__)

# Call the function at application startup
create_database_if_not_exists()

# Determine which database to connect to
db_host = os.getenv('MYSQL_HOST', 'localhost')
db_user = os.getenv('MYSQL_USER', 'root')
db_password = os.getenv('MYSQL_PASSWORD', 'password')
db_name = os.getenv('MYSQL_DATABASE', 'flask_app')

if os.getenv('USE_RDS', 'false') == 'true':
    db_host = os.getenv('RDS_HOST', 'localhost')
    db_user = os.getenv('RDS_USER', 'root')
    db_password = os.getenv('RDS_PASSWORD', 'password')
    db_name = os.getenv('RDS_DATABASE', 'flask_app')

# Configure SQLAlchemy for MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqlconnector://{db_user}:{db_password}@{db_host}/{db_name}'
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
app.secret_key = secrets.token_hex(16)

