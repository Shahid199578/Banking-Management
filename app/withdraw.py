# withdraw.py

from flask import render_template, request, redirect, url_for, flash
from .models import Users, Account, Transactions
from . import db

import random


def generate_random_15_digit_number():
    return random.randint(10**14, 10**15 - 1)

def withdraw(account_number):
    user = Users.query.filter_by(account_number=account_number).first()
    if not user:
        return "User not found"

    account = Account.query.filter_by(account_number=user.account_number).first()
    if not account:
        return "Account not found"

    if request.method == 'POST':
        amount = float(request.form['amount'])
        transaction_type = 'Withdraw'
        if amount > 0:  # Ensure that the withdrawn amount is positive
            if amount <= account.balance:  # Check if the withdrawal amount is less than or equal to the current balance
                reference_number = generate_random_15_digit_number()
                try:
                    # Deduct the withdrawn amount from the account's balance
                    account.balance -= amount

                    # Save transaction details
                    new_transaction = Transactions(
                        account_number=user.account_number,
                        description=f'{transaction_type} of {amount}',
                        balance=account.balance,
                        withdraw=amount,
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
                    return redirect(url_for('withdraw', account_number=account_number))
            else:
                flash('Insufficient balance', 'error')
                return render_template('withdraw.html', user=user, account=account)
        else:
            flash('Invalid withdrawal amount', 'error')
            return render_template('withdraw.html', user=user, account=account)

    return render_template('withdraw.html', user=user, account=account)

