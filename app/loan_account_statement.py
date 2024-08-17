from flask import render_template, request, redirect, url_for, flash
from .models import Users, Account, Transactions
from . import db
import random

def generate_random_15_digit_number():
    return random.randint(10**14, 10**15 - 1)


def loan_account_statement(account_number):
    user = Users.query.filter_by(account_number=account_number).first()
    if not user:
        return "User not found"

    account = Account.query.filter_by(account_number=account_number).first()
    if not account:
        return "Account not found"

    # Fetch the latest loan transaction details from the Transactions table
    loan_transaction = Transactions.query.filter_by(account_number=account_number).filter(Transactions.loan_amount.isnot(None)).order_by(Transactions.date.desc()).first()

    if not loan_transaction:
        return "Loan transaction details not found"

    loan_amount = float(loan_transaction.loan_amount)
    interest_rate = float(loan_transaction.interest_rate) / 100  # Convert to decimal
    tenure = int(loan_transaction.tenure)  # Ensure tenure is an integer

    # Calculate the EMI
    if interest_rate > 0 and tenure > 0:  # Ensure tenure is greater than 0
        monthly_interest_rate = interest_rate / 12
        emi = (loan_amount * monthly_interest_rate * (1 + monthly_interest_rate) ** tenure) / ((1 + monthly_interest_rate) ** tenure - 1)
    else:
        emi = loan_amount / tenure if tenure > 0 else 0  # If no interest, simply divide loan amount by tenure

    # Fetch all loan transactions related to this account
    loan_transactions = Transactions.query.filter_by(account_number=account_number).all()

    # Calculate remaining loan amount
    remaining_loan_amount = sum(float(t.loan_amount) for t in loan_transactions if t.loan_amount)  # Adjust logic as needed
    last_emi = loan_transactions[-1] if loan_transactions else None  # Get the last transaction if exists

    return render_template('loan_account_statement.html', user=user, account=account, loan_transactions=loan_transactions, remaining_loan_amount=remaining_loan_amount, last_emi=last_emi, emi=emi, tenure=tenure)
