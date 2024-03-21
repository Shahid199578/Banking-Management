# deposit.py

from flask import render_template, request, redirect, url_for, flash
from .models import Users, Account, Transactions
from . import db
import random

def generate_random_15_digit_number():
    return random.randint(10**14, 10**15 - 1)



def deposit(account_number):
    user = Users.query.filter_by(account_number=account_number).first()
    if not user:
        return "User not found"

    account = Account.query.filter_by(account_number=user.account_number).first()
    if not account:
        return "Account not found"

    if request.method == 'POST':
        amount = float(request.form['amount'])
        transaction_type = 'Deposit'
        if amount > 0:  # Ensure that the deposited amount is positive
            # Add the deposited amount to the account's balance
            account.balance += amount
            updated_balance = account.balance
            reference_number = generate_random_15_digit_number()
            try:
                # Save transaction details
                new_transaction = Transactions(
                    account_number=user.account_number,
                    description=f'{transaction_type} of {amount}',
                    balance=updated_balance,
                    deposit=amount,
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
                return redirect(url_for('deposit', account_number=account_number))
        else:
            flash('Invalid deposit amount', 'error')

    return render_template('deposit.html', user=user, account=account)

