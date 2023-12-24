from db_manager import DbManager
import random
from datetime import datetime as dt
import sqlite3
from validations import validate_int_params, is_valid_phone_number, is_valid_email


class BankAccounts:
    def __init__(self, database_path, account_holder_name, account_email, account_address, account_phone_number,
                 account_birth_date):
        self.database_path = database_path
        self.db = DbManager(self.database_path)
        """ error handling """
        if not isinstance(account_holder_name, str):
            raise TypeError("account_holder_name must be a string")
        if not is_valid_email(account_email):
            raise Exception("Not a Valid Email")
        if not isinstance(account_address, str):
            raise TypeError("account_address must be a string")
        if not is_valid_phone_number(account_phone_number):
            raise Exception("Not a Valid Phone Number")
        if not isinstance(account_birth_date, dt):
            raise Exception("Not a Valid Birth Date")

        self.account_holder_name = account_holder_name
        self.account_email = account_email
        self.account_address = account_address
        self.account_phone_number = account_phone_number
        self.account_birth_date = account_birth_date
        self.account_pin_code = random.randint(1000, 9999)
        self.account_number = self.create_account(self.account_pin_code, self.account_holder_name, self.account_email,
                                                  self.account_address, self.account_phone_number,
                                                  self.account_birth_date)

    def __str__(self):
        return f"New account was created, account number is: {self.account_number} and your secret pin code is: {self.account_pin_code}"

    def generate_unique_account_number(self):
        while True:
            # Generate a random 4-digit number
            account_number = random.randint(1000, 9999)
            try:
                # Try to insert the generated number into the database
                self.db.execute_query('INSERT INTO dim_account_numbers (account_number) VALUES (?)', (account_number,))

                return account_number
            except sqlite3.IntegrityError:
                # If the number is not unique, continue the loop
                pass

    def create_account(self, account_pin_code, account_holder_name, account_email, account_address,
                       account_phone_number,
                       account_birth_date):
        """
        Creates a new bank account.
        Args:
            account_pin_code:
            account_holder_name: The name of the account holder.
            account_email: The email of the account holder.
            account_address: The address of the account holder.
            account_phone_number: The phone number of the account holder.
            account_birth_date: The birthday of the account holder.
        Returns:
            The bank account number of the newly created account.
        """
        account_number = self.generate_unique_account_number()

        self.db.execute_query("""INSERT INTO dim_accounts (account_number, account_pin_code, account_holder_name,
                                                                account_email, account_address, account_phone_number,
                                                                account_birth_date)
                                VALUES (?,?,?,?,?,?,?)""", (account_number, account_pin_code, account_holder_name,
                                                            account_email, account_address, account_phone_number,
                                                            account_birth_date))

        return account_number


class BankManagementSystem:
    def __init__(self, database_path):
        self.database_path = database_path
        self.db = DbManager(self.database_path)
        # Create DB tables if they are not exist.
        self.create_fact_transactions_table()
        self.create_dim_transactions()
        # Create dim_accounts table if it is not exist.
        self.create_dim_accounts_table()

    def create_fact_transactions_table(self):
        """
                Creates a new account transaction table.
        """
        self.db.execute_query("""CREATE TABLE IF NOT EXISTS fact_transactions (
                            transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
                            account_number INTEGER,
                            transaction_type INTEGER,
                            transaction_date DATETIME,
                            account_balance REAL
                        )""")

    def create_dim_transactions(self):
        """
            Creates a dim transaction table and fill it with data.
        """
        self.db.execute_query("""CREATE TABLE IF NOT EXISTS dim_transactions (
                    transaction_type INTEGER PRIMARY KEY,
                    transaction_desc TEXT
                    )""")
        data_exists = self.db.execute_query("""SELECT * FROM dim_transactions""", None, True)
        if not data_exists:
            self.db.execute_query("""INSERT INTO dim_transactions (transaction_type, transaction_desc)
                                    VALUES  (0, 'Initial Balance'),
                                            (1, 'Deposit'),
                                            (2, 'Withdraw');
                                            """)

    def create_dim_accounts_table(self):
        """
                Creates a new bank account table,
                and a new account numbers table.
        """
        self.db.execute_query("""CREATE TABLE IF NOT EXISTS dim_accounts (
                          account_number INTEGER PRIMARY KEY,
                          account_pin_code INTEGER,
                          account_holder_name TEXT NOT NULL,
                          account_email TEXT NOT NULL,
                          account_address TEXT NOT NULL,
                          account_phone_number TEXT NOT NULL,
                          account_birth_date DATETIME NOT NULL
                      )""")

        self.db.execute_query('''
              CREATE TABLE IF NOT EXISTS dim_account_numbers (
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  account_number INTEGER UNIQUE
              )
          ''')

    def add_new_account(self, account_number):
        self.db.execute_query("""INSERT INTO fact_transactions (account_number,
                                    transaction_type, transaction_date, account_balance)
                                        VALUES (?,?,?,?)""", (account_number,
                                                              0, dt.now(), 0))
        return True

    def update_balance(self, account_number, transaction_type, amount):
        self.db.execute_query("""INSERT INTO fact_transactions(account_number,  
        transaction_type, transaction_date, account_balance) VALUES (?,?,?,?)""",
                              (account_number, transaction_type, dt.now(), amount))
        self.db.db_commit()

    def get_account_balance(self, account_number, account_pin_code):
        """Gets the balance of a bank account.
        Args:
            account_number: The bank account number.
            account_pin_code: Pin code of the customer.
        Returns:
            The balance of the bank account.
        """
        if self.account_lookup(account_number, account_pin_code):
            account_balance = self.db.execute_query("""SELECT account_balance FROM fact_transactions 
            WHERE account_number = ? GROUP BY account_number HAVING transaction_date = max(transaction_date) """,
                                                    (account_number,), False,
                                                    False, True)
            return account_balance[0]
        return -1

    def deposit(self, account_number, account_pin_code, amount):
        """Deposits money into a bank account.
        Args:
            account_number: The bank account number.
            account_pin_code: Pin code of the customer.
            amount: The amount of money to deposit.
        """
        self.db.db_commit()
        try:
            if self.account_lookup(account_number, account_pin_code) and amount > 0.0:
                update_amount = self.get_account_balance(account_number, account_pin_code) + amount
                self.db.db_commit()
                self.update_balance(account_number, 1, update_amount)
                return True
            else:
                raise ValueError("Invalid Account details or Invalid Amount.")

        except ValueError as ve:
            # Handle any other ValueError raised in the try block
            print(ve)
            return False

    def withdraw(self, account_number, account_pin_code, amount):
        """Withdraws money from a bank account.
        Args:
            account_number: The bank account number.
            account_pin_code: Pin code of the customer.
            amount: The amount of money to withdraw.
        """
        try:
            if self.account_lookup(account_number, account_pin_code) and amount > 0:
                update_amount = self.get_account_balance(account_number, account_pin_code) - float(amount)
                if update_amount >= 0:
                    self.update_balance(account_number, 2, update_amount)
                    return True
                else:
                    return False
            else:
                raise ValueError("Invalid Account details or Invalid Amount.")
        except ValueError as ve:
            # Handle any other ValueError raised in the try block
            print(ve)
            return False

    def account_lookup(self, account_number, account_pin_code):
        """Checks if account exists.
                Args:
                    account_number: The bank account number.
                    account_pin_code: Pin code of the customer.
                Returns:
                    The balance of the bank account.True if exists, False otherwise
                """
        if validate_int_params(account_number, account_pin_code):
            if self.db.execute_query(
                    """SELECT * FROM dim_accounts
                    WHERE account_number = ? and account_pin_code = ?""",
                    (account_number, account_pin_code), True):
                return True
            return False
        return False

    def delete_account(self, account_number, account_pin_code):
        """
        Deletes a bank account only from dim_accounts table.
        Args:
            account_number: The account number of the account holder.
            account_pin_code: Pin code of the customer.
        """
        if self.account_lookup(account_number, account_pin_code):
            self.db.execute_query("""DELETE from dim_accounts
                                WHERE account_number = ? and account_pin_code = ?""",
                                  (account_number, account_pin_code))
            return True
        return False
