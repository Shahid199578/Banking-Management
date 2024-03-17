from flask import render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from app import app, db
from .models import Users, Account, Transactions
import os
import random

# Function to generate a random 15-digit number
def generate_random_15_digit_number():
    return random.randint(10**14, 10**15 - 1)

# Define routes

# Specify the path to the uploads folder under the app directory
UPLOAD_FOLDER = os.path.join(app.root_path, '../static', 'uploads')

# Configure the upload folder in app.config
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    total_accounts = Account.query.count()
    total_balance = db.session.query(db.func.sum(Account.balance)).scalar() or 0
    return render_template('dashboard.html', total_accounts=total_accounts, total_balance=total_balance)

@app.route('/all_accounts')
def all_accounts():
    accounts = Account.query.all()
    return render_template('all_accounts.html', accounts=accounts)

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
        mobile_number = request.form.get('mobile_number')
        aadhaar_number = request.form.get('aadhaar_number')
        pan_number = request.form.get('pan_number')
        
        # Ensure both profile picture and signature are uploaded
        if not (profile_picture and signature):
            return "Error: Profile picture and signature files are required."
        
        # Generate unique filenames for uploaded files
        profile_picture_filename = secure_filename(profile_picture.filename)
        signature_filename = secure_filename(signature.filename)
        
        # Save the uploaded files
        profile_picture_path = os.path.join(app.config['UPLOAD_FOLDER'], profile_picture_filename)
        signature_path = os.path.join(app.config['UPLOAD_FOLDER'], signature_filename)
        profile_picture.save(profile_picture_path)
        signature.save(signature_path)

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

        try:
            db.session.add(new_user)
            db.session.commit()

            # Create a new account object for the user
            new_account = Account(
                name=f"{first_name} {last_name}",
                account_type="Regular",
                balance=0
            )
            db.session.add(new_account)
            db.session.commit()

            # Update the account number in the Users table
            new_user.account_number = new_account.account_number
            db.session.commit()

            return redirect(url_for('all_accounts'))
        except Exception as e:
            return f"Error occurred while saving user: {e}"

    # If the request method is GET, render the form template
    return render_template('open_account.html')



@app.route('/all_users')
def all_users():
    # Fetch all users from the database
    users = Users.query.all()
    # Render the HTML template and pass the users
    return render_template('all_users.html', users=users)

@app.route('/view_user_details/<account_number>', methods=['GET', 'POST'])
def view_user_details(account_number):
    user = Users.query.filter_by(account_number=account_number).first()
    if not user:
        return "User not found"
    if request.method == 'POST':
        # Update user details
        return redirect(url_for('view_user_details', account_number=account_number))
    return render_template('view_user_details.html', user=user)

@app.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    user = Users.query.get_or_404(user_id)
    
    if request.method == 'POST':
        # Update user details based on form data
        user.first_name = request.form.get('first_name')
        user.last_name = request.form.get('last_name')
        user.dob = request.form.get('dob')
        user.address = request.form.get('address')
        user.mobile_number = request.form.get('mobile_number')
        user.aadhaar_number = request.form.get('aadhaar_number')
        user.pan_number = request.form.get('pan_number')
        
        # Handle file uploads for profile picture
        if 'profile_picture' in request.files:
            profile_picture = request.files['profile_picture']
            if profile_picture.filename:
                filename = secure_filename(profile_picture.filename)
                profile_picture.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                user.profile_picture = filename
        
        # Handle file uploads for signature
        if 'signature' in request.files:
            signature = request.files['signature']
            if signature.filename:
                filename = secure_filename(signature.filename)
                signature.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                user.signature = filename
        
        # Commit changes to the database
        db.session.commit()
        # Update corresponding account information based on account number
        account = Account.query.filter_by(account_number=user.account_number).first()
        if account:
            account.name = f"{user.first_name} {user.last_name}"
            db.session.commit()
        
        # Redirect to the user details page
        return redirect(url_for('view_user_details', account_number=user.account_number))
    
    # If the request method is GET, render the edit form
    return render_template('edit_user.html', user=user)


'''
@app.route('/withdraw/<int:account_number>', methods=['GET', 'POST'])
def withdraw(account_number):
    user = Users.query.filter_by(account_number=account_number).first()
    if not user:
        return "User not found"
    
    account = Account.query.filter_by(account_number=user.account_number).first()
    if not account:
        return "Account not found"
    
    if request.method == 'POST':
        amount = float(request.form['amount'])
        transaction_type ='Withdraw'
        if amount <= account.balance:  # Check if the withdrawal amount is less than or equal to the current balance
            account.balance -= amount  # Deduct the withdrawal amount from the account's balance
            updated_balance = account.balance
            db.session.commit()

        try:    # Save transaction details
            new_transaction = Transactions(
                account_number=user.account_number,
                description=f'{transaction_type} of {amount}',
                #amount=amount,
		balance = updated_balance,
		withdraw=amount
            )
            db.session.add(new_transaction)
            db.session.commit()
            flash(f'{transaction_type} successful. Reference number: {new_transaction.Reference_number}', 'success')
            return redirect(url_for('all_accounts'))  # Redirect to dashboard or another appropriate page
        except Exception as e:
            db.session.rollback()
            flash('Transaction failed. Please try again later.', 'error')
	    return redirect(url_for('all_accounts'))  # Redirect to dashboard or another appropriate page
        else:
            flash('Insufficient balance' , 'error')
    
    return render_template('withdraw.html', user=user, account=account)

@app.route('/deposit/<int:account_number>', methods=['GET', 'POST'])
def deposit(account_number):
    user = Users.query.filter_by(account_number=account_number).first()
    if not user:
        return "User not found"
    
    account = Account.query.filter_by(account_number=user.account_number).first()
    if not account:
        return "Account not found"
    
    if request.method == 'POST':
        amount = float(request.form['amount'])
        transaction_type='Deposit'
        if amount > 0:  # Ensure that the deposited amount is positive
            account.balance += amount  # Add the deposited amount to the account's balance
            updated_balance = account.balance
            db.session.commit()

        try:    # Save transaction details
            new_transaction = Transactions(
                account_number=user.account_number,
                description=f'{transaction_type} of {amount}',
               # amount=amount,
		balance=updated_balance,
		deposit=amount
            )
            db.session.add(new_transaction)
            db.session.commit()
            flash(f'{transaction_type} successful. Reference number: {new_transaction.Reference_number}', 'success')
	    return redirect(url_for('all_accounts'))  # Redirect to dashboard or another appropriate page
        except Exception as e:
           db.session.rollback()
           flash('Transaction failed. Please try again later.', 'error')
           return redirect(url_for('all_accounts'))  # Redirect to dashboard or another appropriate page
	else:
            flash('Invalid deposit amount', 'error')
    
    return render_template('deposit.html', user=user, account=account)
'''
@app.route('/withdraw/<int:account_number>', methods=['GET', 'POST'])
def withdraw(account_number):
    user = Users.query.filter_by(account_number=account_number).first()
    if not user:
        return "User not found"
    
    account = Account.query.filter_by(account_number=user.account_number).first()
    if not account:
        return "Account not found"
    
    if request.method == 'POST':
        amount = float(request.form['amount'])
        transaction_type ='Withdraw'
        if amount <= account.balance:  # Check if the withdrawal amount is less than or equal to the current balance
            account.balance -= amount  # Deduct the withdrawal amount from the account's balance
            updated_balance = account.balance
	    reference_number = generate_random_15_digit_number()

	    try:
                # Save transaction details
                new_transaction = Transactions(
                    account_number=user.account_number,
                    description=f'{transaction_type} of {amount}',
                    balance=updated_balance,
                    withdraw=amount,
		    reference_number=reference_number
                )
                db.session.add(new_transaction)
                db.session.commit()
                flash(f'{transaction_type} successful. Reference number: {new_transaction.Reference_number}', 'success')
                return redirect(url_for('all_accounts'))  # Redirect to dashboard or another appropriate page
            except Exception as e:
                db.session.rollback()
                flash('Transaction failed. Please try again later.', 'error')
                return redirect(url_for('all_accounts'))  # Redirect to dashboard or another appropriate page
        else:
            flash('Insufficient balance', 'error')
    
    return render_template('withdraw.html', user=user, account=account)

@app.route('/deposit/<int:account_number>', methods=['GET', 'POST'])
def deposit(account_number):
    user = Users.query.filter_by(account_number=account_number).first()
    if not user:
        return "User not found"
    
    account = Account.query.filter_by(account_number=user.account_number).first()
    if not account:
        return "Account not found"
    
    if request.method == 'POST':
        amount = float(request.form['amount'])
        transaction_type='Deposit'
        if amount > 0:  # Ensure that the deposited amount is positive
            account.balance += amount  # Add the deposited amount to the account's balance
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
                flash(f'{transaction_type} successful. Reference number: {new_transaction.Reference_number}', 'success')
                return redirect(url_for('all_accounts'))  # Redirect to dashboard or another appropriate page
            except Exception as e:
                db.session.rollback()
                flash('Transaction failed. Please try again later.', 'error')
                return redirect(url_for('all_accounts'))  # Redirect to dashboard or another appropriate page
        else:
            flash('Invalid deposit amount', 'error')
    
    return render_template('deposit.html', user=user, account=account)

