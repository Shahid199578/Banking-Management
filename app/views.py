from flask import render_template, request, redirect, url_for
from . import app
from .models import User, Account

# Define routes
# Update the query in views.py
@app.route('/')
def dashboard():
    total_accounts = Account.query.count()
    total_balance = db.session.query(db.func.sum(Account.balance)).scalar() or 0
    return render_template('dashboard.html', total_accounts=total_accounts, total_balance=total_balance)

#@app.route('/')
#def dashboard():
#    total_accounts = Account.query.count()
#    total_balance = db.session.query(db.func.sum(Account.balance)).scalar() or 0
#    return render_template('index.html', total_accounts=total_accounts, total_balance=total_balance)

@app.route('/all_accounts')
def all_accounts():
    accounts = Account.query.all()
    return render_template('all_accounts.html', accounts=accounts)

@app.route('/open_account', methods=['GET', 'POST'])
def open_account():
    if request.method == 'POST':
        # Retrieve form data
        # Perform validation
        # Save data to database
        return redirect(url_for('all_accounts'))
    return render_template('open_account.html')

@app.route('/view_user_details/<account_number>', methods=['GET', 'POST'])
def view_user_details(account_number):
    user = User.query.filter_by(account_number=account_number).first()
    if not user:
        return "User not found"
    if request.method == 'POST':
        # Update user details
        return redirect(url_for('view_user_details', account_number=account_number))
    return render_template('view_user_details.html', user=user)

