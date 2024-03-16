from app import db

class Account(db.Model):
    account_number = db.Column(db.Integer, primary_key=True)  # Setting account_number as primary key
    name = db.Column(db.String(100), nullable=False)
    account_type = db.Column(db.String(50), nullable=False)
    balance = db.Column(db.Float, nullable=False)


class Users(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    account_number = db.Column(db.String(20), db.ForeignKey('account.account_number'), nullable=False)
    dob = db.Column(db.String(10))  # Assuming date of birth is a string for simplicity
    address = db.Column(db.String(255))
    profile_picture = db.Column(db.String(255))  # Define profile picture column
    signature = db.Column(db.String(255))  # Define signature column
    mobile_number = db.Column(db.String(15))
    aadhaar_number = db.Column(db.String(20))
    pan_number = db.Column(db.String(20))
