# withdraw.py

from flask import render_template, request, redirect, url_for, flash
from .models import Users, Account, Transactions
from . import db
from app import encrypt, decrypt
import random
from functools import wraps


# # Encrypt account number using cipher
# def encrypt(account_number):
#     return cipher_suite.encrypt(str(account_number).encode()).decode()

# def decrypt(encrypted_account_number):
#     try:
#         return cipher_suite.decrypt(encrypted_account_number.encode()).decode()
#     except Exception as e:
#         print(f"Decryption error: {e}")  # Log the error for debugging
#         return None

def generate_random_15_digit_number():
    return random.randint(10**14, 10**15 - 1)

def withdraw(encrypted_account_number):
    account_number = decrypt(encrypted_account_number)
    if not account_number:
        return "Invalid account number"

    user = Users.query.filter_by(account_number=account_number).first()
    if not user:
        return "User not found"

    account = Account.query.filter_by(account_number=user.account_number).first()
    if not account:
        return "Account not found"

    if request.method == 'POST':
        try:
            amount = float(request.form['amount'])
            transaction_type = 'Withdraw'
            print(f"Attempting to withdraw amount: {amount}, current balance: {account.balance}")
            if amount > 0:
                if amount <= account.balance:
                    reference_number = generate_random_15_digit_number()
                    account.balance -= amount
                    new_transaction = Transactions(
                        account_number=user.account_number,
                        description=f'{transaction_type} of {amount}',
                        balance=account.balance,
                        withdraw=amount,
                        reference_number=reference_number
                    )
                    db.session.add(new_transaction)
                    db.session.commit()
                    flash(f'{transaction_type} successful. Reference number: {reference_number}', 'success')
                    return redirect(url_for('all_accounts'))
                else:
                    flash('Insufficient balance', 'error')
                    print(f"Withdrawal failed: Insufficient balance. Amount: {amount}, Balance: {account.balance}")
                    return render_template('withdraw.html', user=user, account_number=account_number)
            else:
                flash('Invalid withdrawal amount', 'error')
                return render_template('withdraw.html', user=user, account_number=account_number)
        except Exception as e:
            print(f"Exception occurred: {str(e)}")
            db.session.rollback()
            flash('Transaction failed. Please try again later.', 'error')
            return redirect(url_for('withdraw', encrypted_account_number=encrypted_account_number))

    return render_template('withdraw.html', user=user, account=account, encrypt=encrypt)
