from money import Money
from connect import get_db_connection
import format

def get_this_acc(acc_no: int):
    
    cnx = get_db_connection()
    cursor = cnx.cursor()

    query = ("SELECT * FROM Accounts WHERE acc_no = ?")

    res = cursor.execute(query, (acc_no,)).fetchone()

    cursor.close()
    cnx.close()

    return res

def make_deposit(acc_no: int, val: float):
    entry = get_this_acc(acc_no)
    
    if not entry:
        return False

    cnx = get_db_connection()
    cursor = cnx.cursor()
 
    curr_bal = entry['bal']
    new_bal = curr_bal + val
    update_balance = ("UPDATE Accounts SET bal = ? WHERE acc_no = ?")

    cursor.execute(update_balance, (new_bal, acc_no))

    cnx.commit()

    cursor.close()
    cnx.close()

    return True

def make_withdrawal(acc_no: int, val: float):
    entry = get_this_acc(acc_no)

    if not entry:
        return False
    
    cnx = get_db_connection()
    cursor = cnx.cursor()

    curr_bal = entry['bal']

    if curr_bal - val < entry['min_bal']:
        return False

    new_bal = curr_bal - val
    print(new_bal)
    print(acc_no)
    update_balance = ("UPDATE Accounts SET bal = ? WHERE acc_no = ?")

    cursor.execute(update_balance, (new_bal, acc_no))

    cnx.commit()

    cursor.close()
    cnx.close()

    return True

def get_accs_by_user(username):
    cnx = get_db_connection()
    cursor = cnx.cursor()

    query = ("SELECT * FROM Accounts WHERE username = ?")
    cursor.execute(query, (username,))

    acc_info = cursor.fetchall()

    savings_info = []
    checkings_info = []

    for acc in acc_info:
        new_acc = format.format_acc(acc)
        if new_acc['acc_type'].lower() == 'savings':
            savings_info.append(new_acc)
        if new_acc['acc_type'].lower() == 'checkings':
            checkings_info.append(new_acc)

    cursor.close()
    cnx.close()

    return savings_info, checkings_info

def process_new_account(username, acc_type, bal):
    cnx = get_db_connection()
    cursor = cnx.cursor()

    query = ("SELECT * FROM Bank_Settings")
    cursor.execute(query)

    res = cursor.fetchone()

    acc_data = [username, acc_type, None, None, float(bal)]

    if acc_type == 'Savings':
        acc_data[2] = res['savings_rate']
        acc_data[3] = res['savings_min']
    elif acc_type == 'Checkings':
        acc_data[2] = res['checkings_rate']
        acc_data[3] = res['savings_rate']

    add_account = ("INSERT INTO Accounts (username, acc_type, interest_rate, min_bal, bal) VALUES (?, ?, ?, ?, ?)")

    cursor.execute(add_account, acc_data)

    cnx.commit()

    new_acc_no = cursor.lastrowid

    cursor.close()
    cnx.close()

    return new_acc_no

def delete_acc(acc_no):
    cnx = get_db_connection()
    cursor = cnx.cursor()
    
    delete_format = ("DELETE FROM Accounts WHERE acc_no = ?")
    
    cursor.execute(delete_format, (acc_no,))
    
    cnx.commit()

    cursor.close()
    cnx.close()

    return True

def transfer_all(acc_no, transfer_no):
    bal = get_this_acc(acc_no)['bal']
    
    withdrawal_status = make_withdrawal(acc_no, bal)

    if withdrawal_status:
        deposit_status = make_deposit(transfer_no, bal)

        if deposit_status:

            return True

    return False

def transfer(acc_no, transfer_no, bal):
    withdrawal_status = make_withdrawal(acc_no, bal)

    if withdrawal_status:
        deposit_status = make_deposit(transfer_no, bal)

        if deposit_status:

            return True

    return False

#
# TESTED, WORKS, 1/25/23
#
class BankAccount():

    #
    # TESTED, WORKS, 1/25/23
    #
    def __init__(self, new_bal: Money = Money(0.0), new_acc_num: str = "", new_min_bal: Money = Money(0.0), new_ir: float = 0.0):
        """
        Initializer for the General Bank Account Class.
        :param new_bal: The new balance for the account.
        :param min_bal: The minimum balance possible for the account.
        :param new_acc_num: The account number.
        :param new_ir: The interest rate to set on the account.
        """
        self.bal = new_bal
        self.min_bal = new_min_bal
        self.acc_num = new_acc_num
        self.ir = new_ir

    #
    # TESTED, WORKS, 1/25/23
    #
    def deposit(self, amt: Money):
        """
        Deposit an amount of money in this account.
        :param amt: The amount to be deposited.
        """
        self.bal = self.bal + amt
    
    #
    # TESTED, WORKS, 1/25/23
    #
    def withdraw(self, amt: Money) -> bool:
        """
        Withdraw an amount of money from this account.
        :param amt: The amount to be withdrawn.
        :return: False if the amount of money cannot be withdrawn due to the
        minimum allowed balance, True if withdrawal is successful.
        """
        if amt > self.bal - self.min_bal:
            return False
        self.bal -= amt
        return True

    #
    # TESTED, WORKS, 1/25/23
    #
    def compound(self):
        """
        Compound the interest on the account, multiply by interest rate.
        """
        self.bal *= 1 + self.ir

    def format_acc_no(self):
        self.acc_num = self.acc_num.zfill(8)

#
# TESTED, WORKS, 1/25/23
#
class Savings(BankAccount):
    """
    This class is here to identify between checkings and savings and in the
    future this will allow increased functionality. For now it functions
    the same as a bank account.

    NOTE! This savings account functions without withdrawal limits due to the
    2020 revision of Regulation D, which originally placed a 6 withdrawal limit
    per month on a savings account. Post the revision there is no limit on
    withdrawals.
    """

    #
    # TESTED, WORKS, 1/25/23
    #
    def __init__(self, new_bal: Money, new_acc_num: str,
                    new_min_bal: Money = Money(0.0), new_ir: float = 0.0):
        """
        Initializer for the Savings Class.
        :param new_bal: The new balance for the account.
        :param min_bal: The minimum balance possible for the account.
        :param new_acc_num: The account number.
        :param new_ir: The interest rate to set on the account.
        """

        BankAccount.__init__(self, new_bal=new_bal, new_acc_num=new_acc_num,
                                new_min_bal=new_min_bal, new_ir=new_ir)

    #
    # TESTED, WORKS, 1/25/23
    #
    def __str__(self):
        """
        Summarizes the Savings object.
        """
        res = "\nSummary For Account Number - " + self.acc_num + '\n'
        res += "Account Type - Savings\n"
        res += ("Balance On Account : $%.2f" % (self.bal.amt)) + '\n'
        res += ("Interest Rate On Account : %.2f%%" % (100 * self.ir)) + '\n'
        res += ("Minimum Balance Allowed : $%.2f" % (self.min_bal.amt)) + '\n'

        return res

    #
    # TESTED, WORKS, 1/25/23
    #
    def statement(self):
        """
        Get a summary for the account.
        """
        print(self)

    def database_creation(self, cnx, username):
        cursor = cnx.cursor()

        add_account = ("INSERT INTO Accounts (bal, min_bal, interest_rate, acc_type, username) VALUES (%d, %f, %f, %f, %s, %s)")
        account_data = (self.bal.amt, self.min_bal.amt, self.ir, 's', username)
        cursor.execute(add_account, account_data)
        new_acc_no = cursor.lastrowid

#
# TESTED, WORKS, 1/25/23
#
class Checkings(BankAccount):
    """
    This class is here to identify between checkings and savings and in the
    future this will allow increased functionality. For now it functions
    the same as a bank account.
    """

    #
    # TESTED, WORKS, 1/25/23
    #
    def __init__(self, new_bal: Money, new_acc_num: str, 
                    new_min_bal: Money = Money(0.0), new_ir: float = 0.0):
        """
        Initializer for the Checkings Class.
        :param new_bal: The new balance for the account.
        :param min_bal: The minimum balance possible for the account.
        :param new_acc_num: The account number.
        :param new_ir: The interest rate to set on the account.
        """

        BankAccount.__init__(self, new_bal=new_bal, new_acc_num=new_acc_num,
                                new_min_bal=new_min_bal, new_ir=new_ir)

    #
    # TESTED, WORKS, 1/25/23
    #
    def __str__(self):
        """
        Summarizes the Checkings object.
        """
        res = "Summary For Account Number - " + self.acc_num + '\n'
        res += "Account Type - Checkings\n"
        res += ("Balance On Account : $%.2f" % (self.bal.amt)) + '\n'
        res += ("Interest Rate On Account : %.2f%%" % (100 * self.ir)) + '\n'
        res += ("Minimum Balance Allowed : $%.2f" % (self.min_bal.amt)) + '\n'

        return res

    #
    # TESTED, WORKS, 1/25/23
    #
    def statement(self):
        """
        Get a summary for the account.
        """
        print(self)

    def database_creation(self, cnx, username):
        cursor = cnx.cursor()

        add_account = ("INSERT INTO Accounts (bal, min_bal, interest_rate, acc_type, username) VALUES (%d, %f, %f, %f, %s, %s)")
        account_data = (self.bal.amt, self.min_bal.amt, self.ir, 'c', username)
        cursor.execute(add_account, account_data)
        new_acc_no = cursor.lastrowid

        cursor.close()

        return new_acc_no

