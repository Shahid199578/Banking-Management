from flask import Blueprint, render_template
from .models import Users, Account, Transactions
from app import encrypt, decrypt



statement_bp = Blueprint('statement', __name__)

@statement_bp.route('/account_statement/<encrypted_account_number>')
def account_statement(encrypted_account_number):
    account_number = decrypt(encrypted_account_number)

    user = Users.query.filter_by(account_number=account_number).first()
    if not user:
        return "User not found"
    # Retrieve the account based on the account number
    account = Account.query.filter_by(account_number=account_number).first()

    if account:
        
        # Fetch the account statement for the specified account number from the Transactions table
        account_statement = Transactions.query.filter_by(account_number=account_number).all()

        # Render the account statement template with the account details and statement data
        return render_template('account_statement.html', account=account, account_statement=account_statement, encrypt=encrypt)
    else:
        # If the account is not found, render an error page or handle it accordingly
        return render_template('error.html', message='Account not found')

