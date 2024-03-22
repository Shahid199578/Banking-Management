-- Create Database
CREATE DATABASE IF NOT EXISTS bank;

-- Create User
CREATE USER IF NOT EXISTS 'bank'@'localhost' IDENTIFIED BY 'Bank#9911';

-- Grant Privileges
GRANT ALL PRIVILEGES ON `bank`.* TO 'bank'@'localhost';

-- Switch to the 'bank' Database
USE bank;

-- Create Table account_statement
CREATE TABLE IF NOT EXISTS account_statement (
    account_number INT(10) UNSIGNED ZEROFILL NOT NULL,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    description TEXT NOT NULL,
    amount DECIMAL(10,2),
    balance DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    withdraw DECIMAL(10,2),
    deposit DECIMAL(10,2),
    reference_number VARCHAR(20),
    PRIMARY KEY (account_number, date),
    INDEX (account_number)
);

-- Create Table account
CREATE TABLE IF NOT EXISTS account (
    account_number INT(10) UNSIGNED ZEROFILL NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    account_type VARCHAR(50) NOT NULL,
    balance FLOAT NOT NULL DEFAULT 0.0
);

-- Create Table users
CREATE TABLE IF NOT EXISTS users (
    account_number INT(10) UNSIGNED ZEROFILL NOT NULL AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    dob VARCHAR(10),
    address VARCHAR(255),
    mobile_number VARCHAR(15),
    aadhaar_number VARCHAR(20),
    pan_number VARCHAR(20),
    profile_picture VARCHAR(255),
    signature VARCHAR(255)
);

