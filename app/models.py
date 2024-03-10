from app import db

class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account_number = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    account_type = db.Column(db.String(50), nullable=False)
    balance = db.Column(db.Float, nullable=False)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account_number = db.Column(db.String(20), db.ForeignKey('account.account_number'), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    address = db.Column(db.String(200), nullable=False)
    mobile_number = db.Column(db.String(15), nullable=False)
    aadhaar_number = db.Column(db.String(12), nullable=False)
    pan_number = db.Column(db.String(10), nullable=False)

