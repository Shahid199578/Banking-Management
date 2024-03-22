from flask import Blueprint, render_template, request
from .models import Users

search_bp = Blueprint('search', __name__)

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
    return render_template('search.html', users=users)

