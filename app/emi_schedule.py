from flask import render_template
from .models import Users, Account, Transactions, EMISchedule
from app import encrypt, decrypt
from decimal import Decimal, ROUND_HALF_UP
import random
from datetime import timedelta, datetime

def generate_random_15_digit_number():
    return random.randint(10**14, 10**15 - 1)

def emi_schedule(encrypted_account_number):
    account_number = decrypt(encrypted_account_number)
    if not account_number:
        return "Invalid account number"

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

    loan_amount = Decimal(loan_transaction.loan_amount)
    interest_rate = Decimal(loan_transaction.interest_rate) / 100
    tenure = int(loan_transaction.tenure)

    # Calculate EMI
    if interest_rate > 0 and tenure > 0:
        monthly_interest_rate = interest_rate / 12
        emi = (loan_amount * monthly_interest_rate * (1 + monthly_interest_rate) ** tenure) / \
              ((1 + monthly_interest_rate) ** tenure - 1)
    else:
        emi = loan_amount / tenure if tenure > 0 else 0

    emi = emi.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    # Fetch EMI schedule
    emi_schedule = EMISchedule.query.filter_by(account_number=account_number).order_by(EMISchedule.emi_number).all()
    if not emi_schedule:
        return "EMI schedule not found"

    # Calculate remaining loan amount
    pending_emi_amount = sum(Decimal(e.emi_amount) for e in emi_schedule if e.status != 'Paid')
    remaining_loan_amount = pending_emi_amount.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    # Fetch the last EMI payment
    last_emi = Transactions.query.filter_by(account_number=account_number, description="EMI Payment").order_by(Transactions.date.desc()).first()

    # Calculate pending EMIs
    paid_emi_count = Transactions.query.filter_by(account_number=account_number, description="EMI Payment").count()
    pending_emi_count = max(tenure - paid_emi_count, 0)

    # Render the template
    return render_template(
        'emi_schedule.html',
        user=user,
        account=account,
        emi_schedule=emi_schedule,
        remaining_loan_amount=remaining_loan_amount,
        last_emi=last_emi,
        emi=emi,
        tenure=tenure,
        pending_emi_count=pending_emi_count,
        paid_emi_count=paid_emi_count,
        timedelta=timedelta,
        encrypt=encrypt
    )
