<<<<<<< HEAD
#loan_account_statement.py

from flask import render_template
from .models import Users, Account, Transactions
from . import db
from app import encrypt, decrypt
from datetime import timedelta

def loan_account_statement(encrypted_account_number):
    account_number = decrypt(encrypted_account_number)
    if not account_number:
        return "Invalid account number"

    # Fetch the user and account details
=======
from flask import render_template
from .models import Users, Account, Transactions
from . import db
from datetime import timedelta

def loan_account_statement(account_number):
>>>>>>> 8ad0b0d965202959e06c4474165d2b5f64ee123b
    user = Users.query.filter_by(account_number=account_number).first()
    if not user:
        return "User not found"
    
    account = Account.query.filter_by(account_number=account_number).first()
    if not account:
        return "Account not found"

    # Fetch the latest loan transaction details
    loan_transaction = Transactions.query.filter_by(account_number=account_number).filter(Transactions.loan_amount.isnot(None)).order_by(Transactions.date.desc()).first()
    if not loan_transaction:
        return "Loan transaction details not found"

    # Extract loan amount, interest rate, and tenure
    loan_amount = float(loan_transaction.loan_amount)
    interest_rate = float(loan_transaction.interest_rate)  # Convert to decimal
    tenure = int(loan_transaction.tenure)  # Ensure tenure is an integer

<<<<<<< HEAD
    # EMI Calculation
    if interest_rate > 0 and tenure > 0:
        monthly_interest_rate = (interest_rate / 100) / 12
        emi = (loan_amount * monthly_interest_rate * (1 + monthly_interest_rate) ** tenure) / \
              ((1 + monthly_interest_rate) ** tenure - 1)
=======
    # Calculate the EMI and round to the nearest integer
    if interest_rate > 0 and tenure > 0:  # Ensure tenure is greater than 0
        monthly_interest_rate = interest_rate / 12
        emi = (loan_amount * monthly_interest_rate * (1 + monthly_interest_rate) ** tenure) / ((1 + monthly_interest_rate) ** tenure - 1)
>>>>>>> 8ad0b0d965202959e06c4474165d2b5f64ee123b
    else:
        emi = loan_amount / tenure if tenure > 0 else 0

    emi = round(emi)  # Round EMI to the nearest integer

    emi = round(emi)  # Round the EMI to the nearest integer

    # Fetch all loan transactions related to this account
    loan_transactions = Transactions.query.filter_by(account_number=account_number).all()

    # Calculate the total amount paid through EMIs from transactions
    total_paid = sum(float(t.deposit) for t in loan_transactions if t.description == "EMI Payment")

<<<<<<< HEAD
    #fetch total remaining amount
    loan_amount1 = float(loan_transaction.balance)
    # Calculate the remaining loan amount
    remaining_loan_amount = loan_amount1 - total_paid

    # Update the account balance only if it is out of sync
    if abs(remaining_loan_amount - account.balance) > 0.01:  # Tolerance for floating point comparison
        account.balance = remaining_loan_amount
        db.session.commit()

    # Pending EMI Calculation
=======
    # Calculate pending EMIs
>>>>>>> 8ad0b0d965202959e06c4474165d2b5f64ee123b
    paid_emi_count = Transactions.query.filter_by(account_number=account_number, description="EMI Payment").count()
    pending_emi_count = tenure - paid_emi_count

    # Last EMI adjustment
    last_emi_amount = emi if pending_emi_count > 1 else remaining_loan_amount + total_paid - (emi * (tenure - 1))
<<<<<<< HEAD

    # Fetch the last EMI payment
    last_emi = Transactions.query.filter_by(account_number=account_number, description="EMI Payment")\
                                 .order_by(Transactions.date.desc()).first()
    
    # Fetch total_interest_payable
    total_interest_payable = (emi * tenure) - loan_amount

    # Render the template with all required data
=======

    # Fetch the last EMI payment
    last_emi = Transactions.query.filter_by(account_number=account_number, description="EMI Payment").order_by(Transactions.date.desc()).first()

>>>>>>> 8ad0b0d965202959e06c4474165d2b5f64ee123b
    return render_template(
        'loan_account_statement.html',
        user=user,
        account=account,
        loan_transactions=loan_transactions,
        remaining_loan_amount=remaining_loan_amount,
        last_emi=last_emi,
        emi=emi,
        tenure=tenure,
        pending_emi_count=pending_emi_count,
        paid_emi_count=paid_emi_count,
<<<<<<< HEAD
        timedelta=timedelta,
        encrypt=encrypt,
        interest_rate=interest_rate,
        total_interest_payable=round(total_interest_payable),
        loan_amount=loan_amount,
        last_emi_amount=last_emi_amount  # Pass last EMI amount for display
=======
        timedelta=timedelta
>>>>>>> 8ad0b0d965202959e06c4474165d2b5f64ee123b
    )
