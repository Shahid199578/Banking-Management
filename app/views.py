from flask import render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from app import app, db
from .models import Users, Account, Transactions
import os
import random
from sqlalchemy import update
from .deposit import deposit
from .withdraw import withdraw
from . import search
from . import statement
from .open_account import open_account

# Function to generate a random 15-digit number
def generate_random_15_digit_number():
    return random.randint(10**14, 10**15 - 1)

# Define routes

# Specify the path to the uploads folder under the app directory
UPLOAD_FOLDER = os.path.join(app.root_path, '../static', 'uploads')
log_file_path = os.path.join(app.root_path, 'logs', 'app.log')
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

app.route('/open_account', methods=['GET', 'POST'])(open_account)

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
app.route('/deposit/<int:account_number>', methods=['GET', 'POST'])(deposit)
app.route('/withdraw/<int:account_number>', methods=['GET', 'POST'])(withdraw)
app.register_blueprint(search.search_bp)
app.register_blueprint(statement.statement_bp)
