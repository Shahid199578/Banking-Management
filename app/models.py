from app import db

class Account(db.Model):
    account_number = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    account_type = db.Column(db.String(50), nullable=False)
    balance = db.Column(db.Float, nullable=False)

class Users(db.Model):
    __tablename__ = 'users'

    account_number = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    dob = db.Column(db.String(10))
    address = db.Column(db.String(255))
    profile_picture = db.Column(db.String(255))
    signature = db.Column(db.String(255))
    mobile_number = db.Column(db.String(15))
    aadhaar_number = db.Column(db.String(20))
    pan_number = db.Column(db.String(20))



class AccountStatement(db.Model):
    __tablename__ = 'account_statement'
    
    account_number = db.Column(db.Integer, db.ForeignKey('account.account_number'), primary_key=True)
    date = db.Column(db.Date, primary_key=True)
    description = db.Column(db.Text, nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    balance = db.Column(db.Numeric(10, 2), nullable=False)


    def __repr__(self):
        return f"<AccountStatement(account_number={self.account_number}, date={self.date}, description={self.description}, amount={self.amount}, balance={self.balance}, id={self.id})>"
