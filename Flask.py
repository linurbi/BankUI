from flask import Flask, render_template, request
from bank import BankManagementSystem, BankAccounts
from datetime import datetime as dt
from validations import is_valid_birth_date, is_valid_phone_number

database_path = 'db.db'
bm = BankManagementSystem(database_path)

app = Flask(__name__)


@app.route('/', methods=["GET", "POST"])
def home():
    return render_template('index.html')


@app.route('/index', methods=["GET", "POST"])
def index():
    return render_template('index.html')


@app.route('/handle_action', methods=["GET", "POST"])
def handle_action():
    message = ''
    usr_action = request.form.get('action')
    if request.method == 'POST':
        if usr_action == 'new':
            holder_name = request.form.get('holder_name')
            email = request.form.get('email')
            address = request.form.get('address')
            phone = request.form.get('phone')
            birthday = dt.strptime(request.form.get('birthday'), '%Y-%m-%d')
            if is_valid_birth_date(birthday) and is_valid_phone_number(phone):
                ba = BankAccounts(database_path, holder_name, email, address, phone, birthday)
                bm.add_new_account(ba.account_number)
                message = f'You have successfully created a new account, account number is: {ba.account_number} and PIN code is: {ba.account_pin_code} '
            elif not is_valid_birth_date(birthday):
                message = f'Invalid birth date or too young to open an account- You can not create a new account.'
            else:
                message = f'Invalid phone format, should start with 05 and 10 digits.'
        else:
            account_number = int(request.form.get('account_number'))
            pin_code = int(request.form.get('pin_code'))
            if usr_action in ('deposit', 'withdraw'):
                amount = int(request.form.get('amount'))
                # Process deposit
                if usr_action == 'deposit':
                    print(bm.deposit(account_number, pin_code, amount))
                    if bm.deposit(account_number, pin_code, amount):
                        message = f"you have successfully deposited {amount} ILS into your account: {account_number}"
                    else:
                        message = "The action couldn't be completed."
                else:
                    if bm.withdraw(account_number, pin_code, amount):
                        message = f"you have successfully deposited {amount} ILS into your account: {account_number}"
                    else:
                        message = "The action couldn't be completed."
            elif usr_action == 'balance':
                if bm.get_account_balance(account_number, pin_code) >= 0:
                    message = f'Your Current Balance is: {bm.get_account_balance(account_number, pin_code)}'
                else:
                    message = "The action couldn't be completed"
            else:
                if bm.delete_account(account_number, pin_code):
                    message = f'Account Number: {account_number} was successfully removed.'
                else:
                    message = "The action couldn't be completed."
        return render_template('index.html', message=message)


@app.route('/new_account', methods=["GET", "POST"])
def new_account():
    return render_template('new_account.html')


@app.route('/existing_account', methods=["GET", "POST"])
def existing_account():
    usr_action = request.args.get('action')
    if usr_action:
        return render_template('action.html', action=usr_action)
    return render_template('existing_account.html', action=usr_action)


@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run(debug=True)
