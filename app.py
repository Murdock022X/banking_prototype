from flask import Flask, render_template, request, url_for, flash,\
    redirect, session, abort

from connect import get_db_connection

from sys import exit

import format

import users

from accounts import make_deposit, make_withdrawal, get_accs_by_user,\
    get_this_acc, process_new_account, delete_acc, transfer_all, transfer

from bank_settings import get_bank_settings

app = Flask(__name__)
app.config['SECRET_KEY'] = 'octopus'

@app.route('/', methods=('GET', 'POST'))
@app.route('/login/', methods=('GET', 'POST'))
def login():
    """
    Takes user input and processes it to login.
    :return: Rendered web page for login.html that takes username and 
    password input.
    """
    if request.method == 'POST':
        # Get username and password from login.html
        username = request.form['username']
        password = request.form['password']
        
        if not username:
            flash('Please Provide A Username!')
        elif not password:
            flash('Please Provide A Password!')
        else:
            # Get associated user data for username.
            data = users.get_user_data(username)

            # If data is found check password if match then login with user.
            if data:

                if len(data) > 1:
                    flash("ENCOUNTERED MULTIPLE OF THE SAME "
                    "USERNAMES IN DATABASE!")
                    abort(500)
                
                user = data[0]

                if user['password'] == password:
                    
                    session['username'] = user['username']

                    return redirect(url_for('home'))
                
                else:
                    flash("Incorrect Password")
            
            # If username not found in users datatable flash message.
            else:
                flash("Username Not Found")

    # Render the template
    return render_template('login.html')

@app.route('/signup/', methods=('GET', 'POST'))
def signup():
    """
    The signup page for new users. Takes user fields from html page and 
    create new account - see users module.
    :return: The rendered web page that takes input fields.
    """
    if request.method == 'POST':
        # Get username, password, first_name, last_name from signup.html.
        username = request.form['username']
        password = request.form['password']
        first_name = request.form['first_name']
        last_name = request.form['last_name']

        # Flash error messages if any of the fields are missing
        if not username:
            flash('Please Provide A Username')
        elif not password:
            flash('Please Provide A Password')
        elif not first_name:
            flash('Please Provide A First Name')
        elif not last_name:
            flash('Please Provide Last Name')
        
        # If all fields are good attempt to insert.
        else:
            # If inserted is true the insert worked and we flash the message
            # that the user account was created.
            inserted = users.insert_user_data(username, password, first_name, 
                                        last_name)

            if inserted:
                flash("User Account Created")
    
            # If user creation failed then flash the fail message.
            else:
                flash("Username already in use, please select another.")

    return render_template('signup.html')

@app.route('/home/')
def home():
    """
    The home page which has user information about the current user session.
    :return: The rendered template page for home.html.
    """
    # Get user info for the current user session. Pass to the 
    # template so it can be rendered.
    user_info = users.get_user_data(session['username'])[0]
    return render_template('home.html', user_info=user_info)

@app.route('/accounts/')
def accounts():
    """
    Page that displays all accounts for current user. Can also make
    withdrawals and deposits on accounts from this page.
    :return: The rendered web page with all accounts for this user.
    """
    # Get all account info seperated savings and checkings for user.
    savings_info, checkings_info = get_accs_by_user(session['username'])

    # Pass account info to be rendered and return the rendered page.
    return render_template('acc_view.html', savings_info=savings_info,
                    checkings_info=checkings_info)

@app.route('/summary/')
def summary():
    """
    Summarize accounts for current user.
    :return: Rendered web page summary.html.
    """

    # Get the session username.
    username = session['username']

    # The sum of all balances.
    bal_sum = 0.0

    # Get all accounts for user.
    res = users.get_user_accounts(username)

    # Add up balances for all accounts.
    for acc in res:
        bal_sum += float(acc['bal'])

    # Format total balance into money string and render the summary.html page.
    bal_sum = format.format_money(bal_sum)
    return render_template('summary.html', sum=bal_sum, accounts=res)

@app.route('/logout/')
def logout():
    """
    Logout the user.
    """

    if 'username' in session:
        session.pop('username', None)
    return render_template('logout.html')

@app.route('/accounts/create/', methods=('GET', 'POST'))
def create_account():
    """
    The account creation page where users create new bank accounts, can 
    choose between savings and checkings as well as starting balances.
    :return: The rendered web page, create_account.html with 
    relevant info passed.
    """
    if request.method == 'POST':
        # Get the username, balance, and account type (Savings or Checkings).
        username = session['username']
        bal = request.form['bal']
        acc_type = request.form['acc_type']

        # Flash error messages
        if not bal:
            flash('Please Provide A Balance')
        elif not acc_type:
            flash('Please Provide An Account Type')

        # Process the new_account request and format the new account 
        # number to display the message.
        else:
            new_acc = format.format_acc_no(
                process_new_account(username, acc_type, bal))
            flash('New Account Created, Number: ' + new_acc)

    res = get_bank_settings()

    # Render the account creation template.
    return render_template('create_account.html', 
            savings_rate=format.format_ir(res['savings_rate']), 
            savings_min=format.format_money(res['savings_min']),
            checkings_rate=format.format_ir(res['checkings_rate']), 
            checkings_min=format.format_money(res['checkings_min']))

@app.route('/<int:acc_no>/edit/', methods=('GET', 'POST'))
def edit_account(acc_no):
    """
    The route to edit the selected account, can make withdrawals and deposits.
    :param acc_no: The account number to make edits on.
    :return: A rendered web page created from edit_acc.html.
    """
    if request.method == 'POST':
        # Get the edit type from the form (Deposit or Withdrawal)
        edit_type = request.form['type']
        value = 0.0

        # Try to get the deposit or withdrawal amount from 
        # the edit_acc.html form.
        try:
            value = float(request.form['value'])
        except ValueError as err:
            flash("Please Provide A Valid Amount")
        else:
            if not acc_no:
                abort(500)

            # If type is withdrawal make the withdrawal and flash a message.
            # that changes the balance.
            elif edit_type == 'Withdrawal':
                res = make_withdrawal(acc_no, value)
                if res:
                    flash('Withdrawal of $%.2f Made From %s' % (value, format.format_acc_no(acc_no)))
                else:
                    flash('Requested Amount Would Leave Remaining Balance Below Minimum Balance Allowed On Account')
            # If type is deposit make the deposit and flash a message.
            elif edit_type == 'Deposit':
                make_deposit(acc_no, value)
                flash('Deposit of $%.2f Made Into %s' % (value, format.format_acc_no(acc_no)))
            else:
                flash('Please Provide A Valid Request')
    
    # Get the balance on this account and format, pass to the render template 
    # function to render edit_acc.html.
    bal = format.format_money(get_this_acc(acc_no)['bal'])
    return render_template('edit_acc.html', acc_no=format.format_acc_no(acc_no), bal=bal)

@app.route('/<int:acc_no>/delete/', methods=('GET', 'POST'))
def delete_account(acc_no):
    if request.method == 'POST':
        transfer_option = request.form['transfer_option']

        confirm_acc_no = 0
        try:
            confirm_acc_no = int(request.form['acc_no'])
        except ValueError as err:
            flash('Please Enter A Valid Account Number')
        else:
            transfer_no = 0

            if transfer_option == 'Yes':
                try:
                    transfer_no = int(request.form['transfer_no'])
                except ValueError as err:
                    flash('Please Enter A Valid Transfer Account')
                else:
                    transfer_all(acc_no, transfer_no)

            if confirm_acc_no == acc_no:
                res = delete_acc(acc_no)
                if res:
                    return redirect(url_for('accounts'))
                else:
                    abort(500)

            else:
                flash("Account Number Not Correct")
        
    return render_template('delete_acc.html', 
                           acc_no=format.format_acc_no(acc_no))

@app.route('/<int:acc_no>/transfer_acc/', methods=('GET', 'POST'))
def transfer_acc(acc_no):
    if request.method == 'POST':
        transfer_no = request.form['transfer_no']
        transfer_amt = 0.0
        try:
            transfer_amt = float(request.form['transfer_amt'])
        except ValueError as err:
            flash('Please Provide An Amount To Transfer')
        else:
            if not transfer_no:
                flash('Please Provide A Transfer Number')
            else:
                transfer_status = transfer(acc_no, transfer_no, transfer_amt)
                if transfer_status:
                    return redirect(url_for('accounts'))
                else:
                    flash('Transfer Number Invalid')

    bal = get_this_acc(acc_no)['bal']
    return render_template('transfer.html', 
                           acc_no=format.format_acc_no(acc_no), 
                           bal=format.format_money(bal))

@app.route('/project_info/')
def project_info():
    return render_template('project_info.html')
