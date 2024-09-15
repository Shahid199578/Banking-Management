#open_account.py

from flask import request, redirect, url_for, render_template, flash
from werkzeug.utils import secure_filename
from app import app, db
from .models import Users, Account, Transactions, EMISchedule
from datetime import datetime, timedelta
import os
import random
from .notification_service import notify_user_of_account_opening
from decimal import Decimal, ROUND_HALF_UP
from sqlalchemy.exc import SQLAlchemyError

# Function to generate a random 15-digit number
def generate_random_15_digit_number():
    return random.randint(10**14, 10**15 - 1)

# Specify the path to the uploads folder under the app directory
UPLOAD_FOLDER = os.path.join(app.root_path, 'static', 'uploads')

# Create the uploads directory if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Configure the upload folder in app.config
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/open_account', methods=['GET', 'POST'])
def open_account():
    if request.method == 'POST':
        # Retrieve form data
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        dob = request.form.get('dob')
        address = request.form.get('address')
        profile_picture = request.files.get('profile_picture')
        signature = request.files.get('signature')
        mobile_number_digits = request.form.getlist('mobile_number[]')
        mobile_number = ''.join(mobile_number_digits)
        # mobile_number = request.form.get('mobile_number')
        aadhaar_number_digits = request.form.getlist('aadhaar_number[]')
        aadhaar_number = ''.join(aadhaar_number_digits)
        # aadhaar_number = request.form.get('aadhaar_number')
        pan_number_digits = request.form.getlist('pan_number[]')
        pan_number = ''.join(pan_number_digits)
        # pan_number = request.form.get('pan_number')
        account_type = request.form.get('account_type')

        # Check if a user with the same Aadhaar number, PAN number, or mobile number already exists
        existing_user = Users.query.filter(
            (Users.aadhaar_number == aadhaar_number) | 
            (Users.pan_number == pan_number) | 
            (Users.mobile_number == mobile_number)
        ).first()

        if existing_user:
            flash("Alert: User with the same Aadhaar number, PAN number, or mobile number already exists.", 'error')
            return redirect(url_for('all_accounts'))

        # Check if the account type is 'Loan' and set initial_balance accordingly
        if account_type == "Loan":
            initial_balance = Decimal('0')  # Initial balance is not used for loan accounts
        else:
            initial_balance = Decimal(request.form.get('balance', '0'))

        # Ensure both profile picture and signature are uploaded
        if not (profile_picture and signature):
            flash("Error: Profile picture and signature files are required.", 'error')
            return redirect(url_for('open_account'))

        # Retrieve the full name for file naming
        full_name = f"{first_name}_{last_name}"

        # Generate unique filenames for uploaded files
        profile_picture_filename = f"{full_name}_profile_picture_{secure_filename(profile_picture.filename)}"
        signature_filename = f"{full_name}_signature_{secure_filename(signature.filename)}"

        # Save the uploaded files
        profile_picture_path = os.path.join(app.config['UPLOAD_FOLDER'], profile_picture_filename)
        signature_path = os.path.join(app.config['UPLOAD_FOLDER'], signature_filename)

        # Save files to the specified paths
        profile_picture.save(profile_picture_path)
        signature.save(signature_path)



        try:
            # Start a new transaction

            # Create a new user object with the form data
            new_user = Users(
                first_name=first_name,
                last_name=last_name,
                dob=dob,
                address=address,
                profile_picture=profile_picture_filename,
                signature=signature_filename,
                mobile_number=mobile_number,
                aadhaar_number=aadhaar_number,
                pan_number=pan_number
            )

            db.session.add(new_user)
            db.session.flush()

            # Create a new account object for the user
            new_account = Account(
                name=f"{first_name} {last_name}",
                account_type=account_type,
                balance=initial_balance
            )

            db.session.add(new_account)
            db.session.flush()

            # Update the account number in the Users table
            new_user.account_number = new_account.account_number
            db.session.commit()

            if account_type != "Loan":
                # Create initial deposit transaction if not a loan
                initial_deposit = Transactions(
                    account_number=new_account.account_number,
                    date=datetime.now(),
                    description="Initial deposit",
                    amount=initial_balance,
                    balance=initial_balance,
                    deposit=initial_balance,
                    reference_number=generate_random_15_digit_number()
                )

                db.session.add(initial_deposit)
                db.session.commit()
            else:
                # Handle loan account specifics
                loan_amount = Decimal(request.form.get('loan_amount', '0.00'))  # Get loan amount
                interest_rate = Decimal(request.form.get('interest_rate', '0'))  # Get interest rate (as a percentage)
                tenure = int(request.form.get('tenure', '0'))  # Get tenure in months


                # Calculate EMI amount using formula for EMI calculation

                monthly_interest_rate = (interest_rate / Decimal('100')) / Decimal('12')

                emi_amount = (loan_amount * monthly_interest_rate * (Decimal('1') + monthly_interest_rate) ** tenure) / ((Decimal('1') + monthly_interest_rate) ** tenure - Decimal('1'))

                # Calculate total amount with interest (simple interest)

                total_amount_due = emi_amount * Decimal(tenure)

                # Update the account balance with the total amount including interest
                new_account.balance = total_amount_due
                db.session.commit()

                # Create a loan record in Transactions
                loan_transaction = Transactions(
                    account_number=new_account.account_number,
                    date=datetime.now(),
                    description="Loan granted",
                    amount=loan_amount,
                    balance=total_amount_due,  # Updated balance with interest
                    loan_amount=loan_amount,
                    interest_rate=interest_rate,
                    tenure=tenure,
                    reference_number=generate_random_15_digit_number()
                )
                db.session.add(loan_transaction)
                db.session.commit()

                # Generate EMI schedule and save to database

                emi_due_date = datetime.now()
                

                for month in range(1, tenure + 1):  # Loop from 1 to tenure
                    emi_due_date += timedelta(days=30)  # Increment due date by one month
                    emi_schedule_entry = EMISchedule(
                        account_number=new_account.account_number,
                        emi_number=month,  # Assign sequential EMI number starting from 1
                        due_date=emi_due_date,
                        emi_amount=emi_amount,
                    )
                    db.session.add(emi_schedule_entry)
                    

                db.session.commit()
                    


            try:
                notify_user_of_account_opening(new_user, new_account.account_number)
            except Exception as notification_error:
                app.logger.error(f"Notification error: {notification_error}")
                flash("Account opened, but there was an issue notifying the user.", 'warning')

            flash('Account opened successfully', 'success')
            return redirect(url_for('all_accounts'))
        except SQLAlchemyError as e:
            app.logger.error(f"Database error occurred while opening the account: {e}")  # Log the error
            flash(f"Database error occurred while opening the account: {e}", 'error')
            db.session.rollback()  # Rollback in case of an error
        except Exception as e:
            app.logger.error(f"Unexpected error while opening the account: {e}")  # Log the error
            flash(f"Unexpected Error occurred while opening the account: {e}", 'error')
            db.session.rollback()  # Rollback in case of an error

    # If the request method is GET, render the form template
    return render_template('open_account.html')