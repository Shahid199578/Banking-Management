from flask import render_template, request, redirect, url_for, flash
from .models import Users, Account, Transactions
from . import db
import random
from sqlalchemy import and_

def generate_random_15_digit_number():
    return random.randint(10**14, 10**15 - 1)

def emi_payment(account_number):
    user = Users.query.filter_by(account_number=account_number).first()
    if not user:
        return "User not found"

    account = Account.query.filter_by(account_number=user.account_number).first()
    if not account:
        return "Account not found"

    # Fetch the latest loan transaction details
    loan_transaction = Transactions.query.filter_by(account_number=account_number).filter(Transactions.loan_amount.isnot(None)).order_by(Transactions.date.desc()).first()

    if not loan_transaction:
        return "Loan transaction details not found"

    loan_amount = float(loan_transaction.loan_amount)
    interest_rate = float(loan_transaction.interest_rate) / 100  # Convert to decimal
    tenure = int(loan_transaction.tenure)  # Ensure tenure is an integer

    # Calculate the EMI
    if interest_rate > 0 and tenure > 0:
        monthly_interest_rate = interest_rate / 12
        emi = (loan_amount * monthly_interest_rate * (1 + monthly_interest_rate) ** tenure) / ((1 + monthly_interest_rate) ** tenure - 1)
    else:
        emi = loan_amount / tenure if tenure > 0 else 0

    # Calculate the remaining loan amount
    remaining_loan_amount = loan_amount - sum(
        float(t.deposit) for t in Transactions.query.filter(
            and_(Transactions.account_number == account_number, Transactions.description.like('%EMI Payment%'))
        ).all()
    )

    if request.method == 'POST':
        emi_amount = float(request.form['emi_amount'])
        transaction_type = 'EMI Payment'
        if emi_amount > 0:  # Ensure that the EMI amount is positive
            # Subtract the EMI amount from the remaining loan amount
            remaining_loan_amount -= emi_amount
            reference_number = generate_random_15_digit_number()
            try:
                # Save transaction details
                new_transaction = Transactions(
                    account_number=user.account_number,
                    description=transaction_type,
                    balance=remaining_loan_amount,
                    deposit=emi_amount,
                    reference_number=reference_number
                )
                db.session.add(new_transaction)
                db.session.commit()

                # After committing transaction, redirect with reference number as query parameter
                flash(f'{transaction_type} successful. Reference number: {reference_number}', 'success')
                return redirect(url_for('all_accounts'))
            except Exception as e:
                print(f"Exception occurred: {str(e)}")
                db.session.rollback()
                flash('Transaction failed. Please try again later.', 'error')
                return redirect(url_for('emi_payment', account_number=account_number))
        else:
            flash('Invalid EMI amount', 'error')

    return render_template('emi_payment.html', user=user, account=account, remaining_loan_amount=remaining_loan_amount, emi=emi)
