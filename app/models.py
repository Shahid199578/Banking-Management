from . import db
from flask_login import UserMixin
from datetime import datetime

class Account(db.Model):
    account_number = db.Column(db.BigInteger, primary_key=True, autoincrement=True)  # Changed to BigInteger
    name = db.Column(db.String(100), nullable=False)
    account_type = db.Column(db.String(50), nullable=False)
    balance = db.Column(db.Float, nullable=False)

class Users(db.Model):
    __tablename__ = 'users'

    account_number = db.Column(db.BigInteger, primary_key=True, autoincrement=True)  # Changed to BigInteger
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    dob = db.Column(db.String(10))
    address = db.Column(db.String(255))
    profile_picture = db.Column(db.String(255))
    signature = db.Column(db.String(255))
    mobile_number = db.Column(db.String(15))
    aadhaar_number = db.Column(db.String(20))
    pan_number = db.Column(db.String(20))



class Transactions(db.Model):
    __tablename__ = 'account_statement'
    
    account_number = db.Column(db.BigInteger, db.ForeignKey('account.account_number'), primary_key=True)  # Changed to BigInteger
    date = db.Column(db.Date, nullable=False, primary_key=True, default=datetime.now)
    description = db.Column(db.Text, nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=True)
    balance = db.Column(db.Numeric(10, 2), nullable=False)
    withdraw = db.Column(db.Numeric(10, 2), default=0)  # Add withdrawal column with default value 0
    deposit = db.Column(db.Numeric(10, 2), default=0)  # Add deposit column with default value 0
    reference_number = db.Column(db.String(20))
    loan_amount = db.Column(db.Float, nullable=True)  # Add this line
    loan_type = db.Column(db.String(50), nullable=True)  # Add loan type column
    interest_rate = db.Column(db.Numeric(10, 2), nullable=True)  # Add interest rate column
    tenure = db.Column(db.Numeric(10, 2), nullable=True)  # Add tenure column


class AdminUser(db.Model, UserMixin):
    __tablename__ = 'AdminUser'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    def __repr__(self):
        return f"User('{self.username}')"
