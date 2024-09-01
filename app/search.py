from flask import Blueprint, render_template, request
from app import app, db
from .models import Users, Account
search_bp = Blueprint('search', __name__)
from app import encrypt, decrypt


@search_bp.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    users = Users.query.filter(
        Users.account_number.contains(query) |
        Users.first_name.contains(query) |
        Users.last_name.contains(query) |
        Users.mobile_number.contains(query) |
        Users.aadhaar_number.contains(query) |
        Users.pan_number.contains(query)
    ).all()

    # Fetch corresponding account details for each user
    accounts = {}
    for user in users:
        account = Account.query.filter_by(account_number=user.account_number).first()
        if account:
            accounts[user.account_number] = account

    return render_template('search.html', users=users, account=account, encrypt=encrypt, decrypt=decrypt )

