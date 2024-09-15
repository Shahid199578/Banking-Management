from flask import render_template, request, redirect, url_for, flash 
from .models import Users, Account, Transactions, EMISchedule
from app import db, app, encrypt, decrypt
from datetime import datetime
import random
from .notification_service import notify_user_of_transaction

def generate_random_15_digit_number():
    return random.randint(10**14, 10**15 - 1)

def emi_payment(encrypted_account_number):
    account_number = decrypt(encrypted_account_number)
    user = Users.query.filter_by(account_number=account_number).first()
    if not user:
        flash("User not found", 'error')
        return redirect(url_for('all_accounts'))

    account = Account.query.filter_by(account_number=account_number).first()
    if not account:
        flash("Account not found", 'error')
        return redirect(url_for('all_accounts'))

    # Fetch the EMI schedule for this account
    emi_schedule = EMISchedule.query.filter_by(account_number=account_number).order_by(EMISchedule.emi_number).all()
    if not emi_schedule:
        flash("EMI schedule not found", 'error')
        return redirect(url_for('all_accounts'))

    # Determine the number of EMIs paid
    paid_emi_count = EMISchedule.query.filter_by(account_number=account_number, status='Paid').count()
    total_emi_count = len(emi_schedule)

    # Check if all EMIs have been paid
    if paid_emi_count >= total_emi_count:
        flash("No EMIs pending. All EMIs have been paid.", 'info')
        return redirect(url_for('all_accounts'))

    # Get the EMI details for the next pending EMI
    pending_emi = next((emi for emi in emi_schedule if emi.status == 'Pending'), None)
    if not pending_emi:
        flash("No pending EMI found", 'error')
        return redirect(url_for('all_accounts'))

    emi_amount = pending_emi.emi_amount

    if request.method == 'POST':
        try:
            paid_amount = float(request.form['emi_amount'])
            if paid_amount <= 0:
                flash('Invalid EMI amount', 'error')
                return redirect(url_for('emi_payment', encrypted_account_number=encrypted_account_number))

            # Fetch the latest transaction to get the current balance
            latest_transaction = Transactions.query.filter_by(account_number=account_number)\
                                                    .order_by(Transactions.date.desc())\
                                                    .first()
            if not latest_transaction:
                flash("No transaction found for the account", 'error')
                return redirect(url_for('emi_payment', encrypted_account_number=encrypted_account_number))

            remaining_loan_amount = float(latest_transaction.balance)


            # If the remaining loan amount is less than the EMI, adjust to cover the remaining balance
            if remaining_loan_amount <= paid_amount:
                paid_amount = remaining_loan_amount

            # Update remaining loan amount and account balance
            remaining_loan_amount -= paid_amount
            account.balance = remaining_loan_amount
            db.session.commit()

            # Fetch the latest loan transaction details
            loan_transaction = Transactions.query.filter_by(account_number=account_number).filter(Transactions.loan_amount.isnot(None)).order_by(Transactions.date.desc()).first()
            if not loan_transaction:
                flash("Loan transaction details not found", 'error')
                logging.error(f"Loan transaction not found for account {account_number}.")
                
            loan_amount = float(loan_transaction.loan_amount)
            interest_rate = float(loan_transaction.interest_rate)
            tenure = int(loan_transaction.tenure)
  
            
            # Calculate EMI based on interest rate and tenure
            if interest_rate > 0 and tenure > 0:
                monthly_interest_rate = (interest_rate / 100) / 12
                interest_payment = round(loan_amount * monthly_interest_rate)

            # Save transaction details
            principal_payment = paid_amount - interest_payment
            reference_number = generate_random_15_digit_number()

            new_transaction = Transactions(
                account_number=account_number,
                date=datetime.now(),
                description='EMI Payment',
                amount=principal_payment,
                balance=remaining_loan_amount,
                deposit=paid_amount,
                reference_number=reference_number
            )
            db.session.add(new_transaction)

            # Update EMI schedule status to 'Paid'
            pending_emi.status = 'Paid'
            pending_emi.payment_date = datetime.now()
            db.session.commit()

            try:
                notify_user_of_transaction(user, paid_amount, 'emi_payment', updated_balance=account.balance, reference_number=reference_number)
            except Exception as notification_error:
                app.logger.error(f"Notification error: {notification_error}")

            # Success message based on loan closure
            if remaining_loan_amount == 0:
                flash(f'EMI Payment successful. Loan fully paid. Reference number: {reference_number}', 'success')
            else:
                flash(f'EMI Payment successful. Reference number: {reference_number}', 'success')

            return redirect(url_for('all_accounts'))

        except Exception as e:
            print(f"Exception occurred: {str(e)}")
            db.session.rollback()
            flash('Transaction failed. Please try again later.', 'error')
            return redirect(url_for('emi_payment', encrypted_account_number=encrypted_account_number))

    return render_template('emi_payment.html', user=user, account=account, remaining_loan_amount=account.balance, emi=emi_amount, encrypt=encrypt)
