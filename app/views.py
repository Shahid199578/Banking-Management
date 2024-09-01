#view.py
from flask import render_template, request, redirect, url_for, flash, session
from werkzeug.utils import secure_filename
from app import app, db, cipher_suite, encrypt, decrypt
from .models import Users, Account, Transactions, AdminUser
from functools import wraps
import hashlib
import random
import os
from .deposit import deposit
from .withdraw import withdraw
from .emi_payment import emi_payment
from .loan_account_statement import loan_account_statement
from .emi_schedule import emi_schedule
from . import search
from . import statement
from .open_account import open_account
from functools import wraps

# Function to generate a random 15-digit number
def generate_random_15_digit_number():
    return random.randint(10**14, 10**15 - 1)

# Encrypt account number using cipher
def encrypt(account_number):
    return cipher_suite.encrypt(str(account_number).encode()).decode()

def decrypt(encrypted_account_number):
    try:
        return cipher_suite.decrypt(encrypted_account_number.encode()).decode()
    except Exception as e:
        print(f"Decryption error: {e}")  # Log the error for debugging
        return None

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

@app.before_request
def require_login():
    if request.endpoint and request.endpoint != 'login' and request.endpoint != 'logout':
        # Allow access to static files without login
        if not request.path.startswith('/static/') and 'logged_in' not in session:
            return redirect(url_for('login', next=request.url))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        hashed_password = hashlib.sha1(password.encode()).hexdigest()
        # Example authentication logic
        user = AdminUser.query.filter_by(username=username, password=hashed_password).first()
        if user:
            # Store user's authentication status in session
            session['logged_in'] = True
            session['username'] = username
    
            next_url = request.args.get('next')
            if not next_url:
                next_url = url_for('index')
            return redirect(next_url)
        
        else:
            # Authentication failed
            return render_template('login.html', message='Invalid credentials')
    return render_template('login.html')


@app.route('/logout')
def logout():
    # Clear user's session to log them out
    session.clear()
    return redirect(url_for('login'))



# Define routes

# Specify the path to the uploads folder under the app directory
UPLOAD_FOLDER = os.path.join(app.root_path, 'static', 'uploads')
log_file_path = os.path.join(app.root_path, 'logs', 'app.log')

# Create the uploads directory if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Configure the upload folder in app.config
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
@login_required
def dashboard():
    total_accounts = Account.query.count()
    total_balance = db.session.query(db.func.sum(Account.balance)).scalar() or 0
    return render_template('dashboard.html', total_accounts=total_accounts, total_balance=total_balance, username=session['username'])
    
# @app.route('/all_accounts')
# @login_required
# def all_accounts():
#     accounts = Account.query.all()
#     return render_template('all_accounts.html', accounts=accounts, encrypt=encrypt, decrypt=decrypt)

@app.route('/all_accounts')
@login_required
def all_accounts():
    accounts = Account.query.all()
    return render_template('all_accounts.html', accounts=accounts, encrypt=encrypt, decrypt=decrypt)



@app.route('/all_transaction')
@login_required
def all_transaction():
    transaction = Transactions.query.all()
    return render_template('all_transaction.html', transaction=transaction)

app.route('/open_account', methods=['GET', 'POST'])(open_account)


@app.route('/all_users')
@login_required
def all_users():
    # Fetch all users from the database
    users = Users.query.all()
    # Render the HTML template and pass the users
    return render_template('all_users.html', users=users, encrypt=encrypt)

@app.route('/view_user_details/<encrypted_account_number>', methods=['GET'])
@login_required
def view_user_details(encrypted_account_number):
    account_number = decrypt(encrypted_account_number)  # Decrypt the account number
    print(f"Encrypted Account Number from URL: {encrypted_account_number}")
    print(f"Decrypted Account Number: {account_number}")
    user = Users.query.filter_by(account_number=account_number).first()
    if not user:
        return "User not found"
    account = Account.query.filter_by(account_number=user.account_number).first()
    if not account:
        return "Account not found"
    return render_template('view_user_details.html', user=user, account=account, encrypt=encrypt, decrypt=decrypt)

@app.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
@login_required
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
        return redirect(url_for('view_user_details', encrypted_account_number=encrypt(user.account_number)))
    
    # If the request method is GET, render the edit form
    return render_template('edit_user.html', user=user)

app.route('/deposit/<encrypted_account_number>', methods=['GET', 'POST'])(deposit)
app.route('/withdraw/<encrypted_account_number>', methods=['GET', 'POST'])(withdraw)
app.route('/emi_payment/<encrypted_account_number>', methods=['GET', 'POST'])(emi_payment)
app.route('/loan_account_statement/<encrypted_account_number>', methods=['GET', 'POST'])(loan_account_statement)
app.route('/emi_schedule/<encrypted_account_number>', methods=['GET' , 'POST'])(emi_schedule)
app.register_blueprint(search.search_bp)
app.register_blueprint(statement.statement_bp)
