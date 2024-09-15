from flask import render_template, flash
from .models import Users, Account, Transactions, EMISchedule
from . import db
from app import encrypt, decrypt
from datetime import datetime, timedelta
from sqlalchemy.sql import text  # Import the text function
import logging

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
        flash("Loan transaction details not found", 'error')
        logging.error(f"Loan transaction not found for account {account_number}.")
        return "Loan transaction details not found"

    # Extract loan details
    loan_amount = float(loan_transaction.loan_amount)
    interest_rate = float(loan_transaction.interest_rate)
    tenure = int(loan_transaction.tenure)
    # remaining_loan_amount = (loan_transaction.balance)

    # Fetch EMI schedule
    emi_schedule = EMISchedule.query.filter_by(account_number=account_number).order_by(EMISchedule.emi_number).all()
    if not emi_schedule:
        return "EMI schedule not found"

    pending_emi_amount = sum(e.emi_amount for e in emi_schedule if e.status != 'Paid')
    # Remaining loan amount
    remaining_loan_amount = round(pending_emi_amount, 2)

    # Calculate pending EMI count and last EMI amount
    paid_emi_count = EMISchedule.query.filter_by(account_number=account_number, status='Paid').count()
    pending_emi_count = len(emi_schedule) - paid_emi_count
    last_emi_amount = remaining_loan_amount if pending_emi_count == 1 else emi_schedule[-1].emi_amount

    # Total Interest Payable Calculation
    total_interest_payable = (emi_schedule[0].emi_amount * tenure) - loan_amount

    # Fetch last EMI payment
    last_emi = Transactions.query.filter_by(account_number=account_number, description="EMI Payment").order_by(Transactions.date.desc()).first()

    # Render the template with all required data
    return render_template(
        'loan_account_statement.html',
        user=user,
        account=account,
        loan_transactions=Transactions.query.filter_by(account_number=account_number).all(),
        remaining_loan_amount=remaining_loan_amount,
        last_emi=last_emi,
        emi=emi_schedule[0].emi_amount,
        tenure=tenure,
        pending_emi_count=pending_emi_count,
        paid_emi_count=paid_emi_count,
        encrypt=encrypt,
        interest_rate=interest_rate,
        total_interest_payable=round(total_interest_payable),
        loan_amount=loan_amount,
        last_emi_amount=last_emi_amount
    )
