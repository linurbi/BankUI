# BankUI
Bank Management with Flask

# Project
The goal of this project is to create a simplified command-line-based bank management system using Python.
The system will be designed using object-oriented programming principles and will utilize a SQLite database for data storage.
This project will provide you with hands-on experience in building and managing a banking application.


# BankManagementSystemPython
A simple Bank Management System with all the basic functions built in Python, sotres data in SQLite.

	Create: Create an account, need the following inputs: account holder name, address, email, mobile-phone and birth date.
	Deposit: to deposit the specified amount into their account.
	Withdraw: to withdraw the specified amount from an account. 
 		 If the user does not have sufficient balance to withdraw they can't withdraw money.
	Check balance: to check the current available balance of the account.

# Instructions
Account Creation:
 	Users should be able to create bank accounts by providing a full name, Email, address, phone number and birth date
 	Account numbers must be unique, auto-generated   initial balance will be 0
 	a secret PIN will be also generated and given to the user
 	Account information should be stored in an SQLite database
Deposit and Withdrawal:
 	Users should be able to deposit and withdraw money from their accounts
 	The system should update the account balance accordingly in the database
 	We don’t allow overdraft
serialization and persistence of data
Balance Inquiry:
 	Users should be able to check the balance of their accounts by providing the account number and secret PIN code
 	The system should retrieve and display the account balance from the database
Account Closure:
 	Users should be able to close their accounts by providing the account number
 	The system should remove the account from the database
Error Handling:
 	Implement proper error handling to handle cases such as invalid account numbers, insufficient funds for withdrawals, and non- existent accounts for inquiries and closures as well as data types safety
Database Interaction:
 	Create a SQLite database to store account information
 	Implement a Python class that handles database connection, table creation, and CRUD (Create, Read, Update, Delete) operations
Clean OOP Design:
 	Implement a well-structured object-oriented design for the bank management system, with classes representing accounts and the bank itself
 	Ensure encapsulation and proper use of object-oriented principle
User Friendly Interface:
 	Provide a simple and user-friendly command-line interface for interacting with the bank system
Logic & UI Separation:
 	Make sure you are separating the class attributes and methods from the UI. Object such as Bank, Account, DB connection etc. SHOULD NOT use prints, inputs and file IO (except for DB operations)


# Requirements
Python 3

# Usage
Clone the repo. Fire up your terminal and type the following:

python main.py

and then you can use very easily
