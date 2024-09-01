<<<<<<< HEAD
from flask import render_template
from .models import Users, Account, Transactions
from app import encrypt, decrypt
from decimal import Decimal, ROUND_HALF_UP
=======
from flask import render_template, request, redirect, url_for, flash
from .models import Users, Account, Transactions
from . import db
>>>>>>> 8ad0b0d965202959e06c4474165d2b5f64ee123b
import random
from datetime import timedelta

def generate_random_15_digit_number():
    return random.randint(10**14, 10**15 - 1)

<<<<<<< HEAD
def emi_schedule(encrypted_account_number):
    account_number = decrypt(encrypted_account_number)
=======


def emi_schedule(account_number):
>>>>>>> 8ad0b0d965202959e06c4474165d2b5f64ee123b
    user = Users.query.filter_by(account_number=account_number).first()
    if not user:
        return "User not found"

    account = Account.query.filter_by(account_number=account_number).first()
    if not account:
        return "Account not found"

    # Fetch loan transaction details
    loan_transaction = Transactions.query.filter_by(account_number=account_number).filter(Transactions.loan_amount.isnot(None)).order_by(Transactions.date.desc()).first()
    if not loan_transaction:
        return "Loan transaction details not found"

<<<<<<< HEAD
    loan_amount = Decimal(loan_transaction.loan_amount)
    interest_rate = Decimal(loan_transaction.interest_rate) / 100
=======
    loan_amount = float(loan_transaction.loan_amount)
    interest_rate = float(loan_transaction.interest_rate) / 100
>>>>>>> 8ad0b0d965202959e06c4474165d2b5f64ee123b
    tenure = int(loan_transaction.tenure)

    # Calculate EMI
    if interest_rate > 0 and tenure > 0:
        monthly_interest_rate = interest_rate / 12
<<<<<<< HEAD
        emi = (loan_amount * monthly_interest_rate * (1 + monthly_interest_rate) ** tenure) / \
              ((1 + monthly_interest_rate) ** tenure - 1)
    else:
        emi = loan_amount / tenure if tenure > 0 else 0

    emi = emi.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    
    # Fetch all loan transactions related to this account
    loan_transactions = Transactions.query.filter_by(account_number=account_number).all()

    # Calculate remaining loan amount
    total_paid = sum(Decimal(t.deposit) for t in loan_transactions if t.description == "EMI Payment")
    #fetch total remaining amount
    loan_amount1 = Decimal(loan_transaction.balance)
    # Calculate the remaining loan amount
    remaining_loan_amount = loan_amount1 - total_paid
    
    remaining_loan_amount = remaining_loan_amount.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
=======
        emi = (loan_amount * monthly_interest_rate * (1 + monthly_interest_rate) ** tenure) / ((1 + monthly_interest_rate) ** tenure - 1)
    else:
        emi = loan_amount / tenure if tenure > 0 else 0

    # Fetch all loan transactions related to this account
    loan_transactions = Transactions.query.filter_by(account_number=account_number).all()

     # Calculate remaining loan amount
    total_paid = sum(float(t.deposit) for t in loan_transactions if t.description == "EMI Payment")
    remaining_loan_amount = loan_amount - total_paid
>>>>>>> 8ad0b0d965202959e06c4474165d2b5f64ee123b

    # Fetch the last EMI payment
    last_emi = Transactions.query.filter_by(account_number=account_number, description="EMI Payment").order_by(Transactions.date.desc()).first()

    # Calculate pending EMIs
    paid_emi_count = Transactions.query.filter_by(account_number=account_number, description="EMI Payment").count()
<<<<<<< HEAD
    pending_emi_count = max(tenure - paid_emi_count, 0)
    
    # Render the template
    return render_template(
        'emi_schedule.html',
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
        encrypt=encrypt
    )
=======
    pending_emi_count = tenure - paid_emi_count
    
    #return render_template('emi_schedule.html', user=user, account=account, loan_transactions=loan_transactions, emi=emi, tenure=tenure, timedelta=timedelta)
    return render_template('emi_schedule.html', user=user, account=account, loan_transactions=loan_transactions, remaining_loan_amount=remaining_loan_amount, last_emi=last_emi, emi=emi, tenure=tenure, pending_emi_count=pending_emi_count, paid_emi_count=paid_emi_count, timedelta=timedelta)
>>>>>>> 8ad0b0d965202959e06c4474165d2b5f64ee123b
