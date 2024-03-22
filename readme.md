# Banking Application

This is a banking application built with Flask that allows users to perform various banking operations such as opening accounts, making deposits, withdrawals, and searching for account details.

## Features

- User Registration: Users can register accounts with their personal information.
- Account Opening: Registered users can open new accounts.
- Deposits and Withdrawals: Users can deposit and withdraw funds from their accounts.
- Search Functionality: Users can search for account details using account numbers, names, mobile numbers, Aadhaar numbers, etc.
- Admin Panel: Admins can manage user accounts and transactions.

## Technologies Used

- Flask: A micro web framework for Python.
- SQLAlchemy: SQL toolkit and Object-Relational Mapping (ORM) library for Python.
- MySQL: A relational database management system.
- HTML/CSS: For the front-end user interface.
- JavaScript: For dynamic client-side behavior.
- jQuery: A JavaScript library for simplifying HTML document traversal and manipulation.

#Project Structure

```
.
├── app                     
│   ├── __init__.py         
│   ├── deposit.py          
│   ├── models.py           
│   ├── search.py           
│   ├── static              
│   │   ├── css             
│   │   ├── js              
│   │   └── uploads         
│   ├── templates           
│   │   ├── all_accounts.html      
│   │   ├── all_users.html         
│   │   ├── dashboard.html         
│   │   ├── deposit.html           
│   │   ├── edit_user.html         
│   │   ├── index.html             
│   │   ├── navbar.html            
│   │   ├── open_account.html      
│   │   ├── search.html            
│   │   ├── view_user_details.html 
│   │   └── withdraw.html          
│   ├── views.py            
│   └── withdraw.py         
├── flask_app.wsgi          
├── setup_flask_app.sh     
└── static                  
    ├── css                 
    ├── js                  
    └── uploads             
```

## Description

### `app` Directory

- **`__init__.py`**: Initialization file for the Flask application.
- **`deposit.py`**: Flask route and logic for handling deposits.
- **`models.py`**: SQLAlchemy models for database tables.
- **`search.py`**: Flask route and logic for search functionality.
- **`static`**: Directory containing static assets such as CSS, JavaScript, and uploaded files.
- **`templates`**: HTML templates for rendering pages.
- **`views.py`**: Flask route definitions and view functions.
- **`withdraw.py`**: Flask route and logic for handling withdrawals.

### `static` Directory

- **`css`**: Directory for CSS stylesheets.
- **`js`**: Directory for JavaScript files.
- **`uploads`**: Directory for file uploads.

## Setup and Deployment

- **`flask_app.wsgi`**: WSGI script file for deploying Flask app.
- **`setup_flask_app.sh`**: Script for setting up Flask app environment.
- **`/etc/apache2/sites-available/flask_app.conf`**: cofigure this as per your requirement i.e. `localhost`.

## Usage

1. Clone the repository.
2. Set up the Flask environment using `setup_flask_app.sh`.
3. Access the application in your web browser.

## Contributing

Contributions are welcome! Please fork the repository and create a pull request with your proposed changes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

