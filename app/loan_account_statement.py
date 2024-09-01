from flask import render_template
from .models import Users, Account, Transactions
from . import db
from app import encrypt, decrypt
from datetime import timedelta

def loan_account_statement(encrypted_account_number):
    account_number = decrypt(encrypted_account_number)
    if not account_number:
        return "Invalid account number"
    
    user = Users.query.filter_by(account_number=account_number).first()
    if not user:
        return "User not found"
    
    account = Account.query.filter_by(account_number=account_number).first()
    if not account:
        return "Account not found"

    # Fetch the latest loan transaction details
    loan_transaction = Transactions.query.filter_by(account_number=account_number, description="Loan granted").order_by(Transactions.date.desc()).first()
    if not loan_transaction:
        return "Loan transaction details not found"

    # Extract loan details
    loan_amount = float(loan_transaction.loan_amount)
    interest_rate = float(loan_transaction.interest_rate)
    tenure = int(loan_transaction.tenure)

    # EMI Calculation
    if interest_rate > 0 and tenure > 0:
        monthly_interest_rate = (interest_rate / 100) / 12
        emi = (loan_amount * monthly_interest_rate * (1 + monthly_interest_rate) ** tenure) / \
              ((1 + monthly_interest_rate) ** tenure - 1)
    else:
        emi = loan_amount / tenure if tenure > 0 else 0
    
    emi = round(emi)

    # Fetch all loan transactions related to this account
    loan_transactions = Transactions.query.filter_by(account_number=account_number).all()

    # Total Paid Calculation
    total_paid = sum(float(t.deposit) for t in loan_transactions if t.description == "EMI Payment")

      #fetch total remaining amount

    loan_amount1 = float(loan_transaction.balance)

    # Calculate the remaining loan amount

    remaining_loan_amount = loan_amount1 - total_paid

    # Correct account balance if needed
    if abs(remaining_loan_amount - account.balance) > 0.01:
        account.balance = remaining_loan_amount
        db.session.commit()

    # Pending EMIs Calculation
    paid_emi_count = Transactions.query.filter_by(account_number=account_number, description="EMI Payment").count()
    pending_emi_count = tenure - paid_emi_count

    # Last EMI Adjustment
    if pending_emi_count == 1:
        last_emi_amount = remaining_loan_amount
    else:
        last_emi_amount = emi

    # Total Interest Payable Calculation
    total_interest_payable = (emi * tenure) - loan_amount

    # Fetch last EMI payment
    last_emi = Transactions.query.filter_by(account_number=account_number, description="EMI Payment").order_by(Transactions.date.desc()).first()

    # Render the template with all required data
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
        timedelta=timedelta,
        encrypt=encrypt,
        interest_rate=interest_rate,
        total_interest_payable=round(total_interest_payable),
        loan_amount=loan_amount,
        last_emi_amount=last_emi_amount  # Pass last EMI amount for display
    )
