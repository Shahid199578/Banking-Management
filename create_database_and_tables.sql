CREATE DATABASE IF NOT EXISTS flask_app;
use flask_app; 
CREATE TABLE account_statement (
    account_number INT(10) UNSIGNED ZEROFILL NOT NULL,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    description TEXT NOT NULL,
    amount DECIMAL(10,2),
    balance DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    withdraw DECIMAL(10,2) DEFAULT 0.00,
    deposit DECIMAL(10,2) DEFAULT 0.00,
    reference_number VARCHAR(20),
    loan_amount FLOAT DEFAULT NULL,           -- Add loan amount
    loan_type VARCHAR(50) DEFAULT NULL,      -- Add loan type
    interest_rate DECIMAL(10,2) DEFAULT NULL, -- Add interest rate
    tenure INT DEFAULT NULL,                  -- Add tenure
    PRIMARY KEY (account_number, date),
    INDEX (account_number)
);


CREATE TABLE account (
    account_number BIGINT UNSIGNED ZEROFILL NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    account_type VARCHAR(50) NOT NULL,
    balance FLOAT NOT NULL DEFAULT 0.0
) AUTO_INCREMENT = 182101505134;

CREATE TABLE users (
    account_number BIGINT UNSIGNED ZEROFILL NOT NULL AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    dob VARCHAR(10),
    address VARCHAR(255),
    mobile_number VARCHAR(15),
    aadhaar_number VARCHAR(20),
    pan_number VARCHAR(20),
    profile_picture VARCHAR(255),
    signature VARCHAR(255)
) AUTO_INCREMENT = 182101505134;
CREATE TABLE `AdminUser` (
  id INT AUTO_INCREMENT PRIMARY KEY,
  username varchar(50) NOT NULL,
  password varchar(100) NOT NULL,
  is_admin tinyint(1) DEFAULT '0'
);




-- Sample entry for the AdminUser table
INSERT INTO AdminUser (username, password, is_admin) VALUES ('user1', SHA1('password'), 0);

-- Sample entry for the account table
INSERT INTO account (account_number, name, account_type, balance) VALUES
(1821014501, 'John Doe', 'Savings', 5000.00),
(1821014502, 'Jane Smith', 'Current', 10000.00),
(1821014503, 'Alice Johnson', 'Savings', 7500.00),
(1821014504, 'Farzi Loan', 'Loan', 15409.00);
(1821014505, 'waste Loan', 'Loan', 17249.00);
(1821014506, 'sasta Loan', 'Loan', 15993.00);

-- Sample entry for the users table
INSERT INTO users (account_number, first_name, last_name, dob, address, mobile_number, aadhaar_number, pan_number, profile_picture, signature) VALUES
(1821014501, 'John', 'Doe', '1990-05-15', '123 Main St, City, Country', '+1234567890', '1234 5678 9012', 'ABCDE1234F', 'Mohd_SHhw_profile_picture_Screenshot_2024-08-31_163420.jpg', 'Mohd_SHhw_signature_Screenshot_2024-08-31_172912.jpg'),
(1821014502, 'Jane', 'Smith', '1985-09-25', '456 Elm St, City, Country', '+1987654321', '5678 9012 3456', 'FGHIJ5678K', 'Mohd_SHhw_profile_picture_Screenshot_2024-08-31_163420.jpg', 'Mohd_SHhw_signature_Screenshot_2024-08-31_172912.jpg'),
(1821014503, 'Alice', 'Johnson', '1995-02-10', '789 Oak St, City, Country', '+1122334455', '9012 3456 7890', 'LMNOP6789Q', 'Mohd_SHhw_profile_picture_Screenshot_2024-08-31_163420.jpg', 'Mohd_SHhw_signature_Screenshot_2024-08-31_172912.jpg'),
(1821014504, 'Farzi', 'Loan', '1995-03-10', '789 Oak St, City, Country', '+1122334455', '9012 3456 7890', 'LMNOP6789P', 'Mohd_SHhw_profile_picture_Screenshot_2024-08-31_163420.jpg', 'Mohd_SHhw_signature_Screenshot_2024-08-31_172912.jpg');
(1821014505, 'waste', 'Loan', '1995-03-10', '789 Oak St, City, Country', '+1122334455', '9012 3456 7890', 'LMNOP6789P', 'Mohd_SHhw_profile_picture_Screenshot_2024-08-31_163420.jpg', 'Mohd_SHhw_signature_Screenshot_2024-08-31_172912.jpg');
(1821014506, 'Sasta', 'Loan', '1995-03-10', '789 Oak St, City, Country', '+1122334455', '9012 3456 7890', 'LMNOP6789P', 'Mohd_SHhw_profile_picture_Screenshot_2024-08-31_163420.jpg', 'Mohd_SHhw_signature_Screenshot_2024-08-31_172912.jpg');
-- Sample entry for the account_statement table
INSERT INTO account_statement (account_number, date, description, amount, balance, withdraw, deposit, reference_number, loan_amount, loan_type, interest_rate, tenure) VALUES
(1821014501, NOW(), 'Initial Deposit', 5000.00, 5000.00, 0, 0, 'REF123456', NULL, NULL, NULL, NULL),
(1821014502, NOW(), 'Initial Deposit', 10000.00, 10000.00, 0, 0, 'REF345678', NULL, NULL, NULL, NULL),
(1821014503, NOW(), 'Initial Deposit', 7500.00, 7500.00, 0, 0, 'REF901234', NULL, NULL, NULL, NULL),
(1821014504, NOW(), 'Loan granted', 15000.00, 15409.00, 0, 0, 'LOAN123456', 15000.00, 'Personal Loan', 5.00, 12);
(1821014505, NOW(), 'Loan granted', 15000.00, 17249.00, 0, 0, 'LOAN123457', 15000.00, 'Personal Loan', 20.00, 17);
(1821014506, NOW(), 'Loan granted', 15000.00, 15993.00, 0, 0, 'LOAN123458', 15000.00, 'Personal Loan', 12.00, 12);

