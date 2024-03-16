from flask import render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from app import app, db
from .models import Users, Account
import os

# Define routes

# Specify the path to the uploads folder under the app directory
UPLOAD_FOLDER = os.path.join(app.root_path, 'uploads')

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

        # Create a new account object with the form data
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
            return redirect(url_for('all_accounts'))
        except Exception as e:
            return f"Error occurred while saving user: {e}"

    # If the request method is GET, render the form template
    return render_template('open_account.html')

@app.route('/all_users')
def all_users():
    # Fetch all users from the database
    user = Users.query.all()
    # Render the HTML template and pass the users
    return render_template('all_users.html', user=user)

@app.route('/view_user_details/<account_number>', methods=['GET', 'POST'])
def view_user_details(account_number):
    user = Users.query.filter_by(account_number=account_number).first()
    if not user:
        return "User not found"
    if request.method == 'POST':
        # Update user details
        return redirect(url_for('view_user_details', account_number=account_number))
    return render_template('view_user_details.html', user=user)

