from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
# Initialize Flask app
app = Flask(__name__)

# Configure SQLAlchemy for MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://bank:Bank#9911@localhost/bank'  # Replace with your MySQL connection string
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking (optional but recommended)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
# Import views
from . import views

# Import models (if necessary)
from . import models

# Ensure all models are created in the database
with app.app_context():
    db.create_all()

