from app import db

class Account(db.Model):
    account_number = db.Column(db.Integer, primary_key=True)  # Setting account_number as primary key
    name = db.Column(db.String(100), nullable=False)
    account_type = db.Column(db.String(50), nullable=False)
    balance = db.Column(db.Float, nullable=False)

"""
class Users(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    account_number = db.Column(db.String(20), db.ForeignKey('account.account_number'), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    address = db.Column(db.String(200), nullable=False)
    mobile_number = db.Column(db.String(15), nullable=False)
    aadhaar_number = db.Column(db.String(12), nullable=False)
    pan_number = db.Column(db.String(10), nullable=False)


class Users(db.Model):
#    __tablename__ = 'users'

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
"""
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    account_number = db.Column(db.Integer, db.ForeignKey('account.account_number'), nullable=False)  # Assuming this is a foreign key to the Account model
    dob = db.Column(db.String(10), nullable=False)  # Assuming date of birth is a string for simplicity
    address = db.Column(db.String(255), nullable=False)
    profile_picture = db.Column(db.String(255), nullable=False)  # Define profile picture column
    signature = db.Column(db.String(255), nullable=False)  # Define signature column
    mobile_number = db.Column(db.String(15), nullable=False)
    aadhaar_number = db.Column(db.String(20), nullable=False)
    pan_number = db.Column(db.String(20), nullable=False)
"""
    def __init__(self, first_name, last_name, dob, address, profile_picture, signature, mobile_number, aadhaar_number, pan_number):
        self.first_name = first_name
        self.last_name = last_name
        self.dob = dob
        self.address = address
        self.profile_picture = profile_picture
        self.signature = signature
        self.mobile_number = mobile_number
        self.aadhaar_number = aadhaar_number
        self.pan_number = pan_number


"""
