import accounts
from connect import get_db_connection
from format import format_acc

def get_user_data(username):
    cnx = get_db_connection()
    cursor = cnx.cursor()
    
    query = ("SELECT * FROM Users WHERE username = ?")
    cursor.execute(query, (username,))
    info = cursor.fetchall()

    cursor.close()
    cnx.close()

    return info

def insert_user_data(username, password, first_name, last_name):
    if len(get_user_data(username)) >= 1:
        return False
    else:
        cnx = get_db_connection()
        cursor = cnx.cursor()
        
        add_user = ("INSERT INTO Users (username, password, first_name, "
        "last_name) VALUES (?, ?, ?, ?)")
        cursor.execute(add_user, (username, password, first_name, last_name))

        cnx.commit()

        cursor.close()
        cnx.close()

        return True

def get_user_accounts(username):
    cnx = get_db_connection()
    cursor = cnx.cursor()

    query = ("SELECT * FROM Accounts WHERE username = ?")
    cursor.execute(query, (username,))

    res = cursor.fetchall()

    cursor.close()
    cnx.close()

    data = []
    for acc in res:
        data.append(format_acc(acc))
        
    return data

class BankUser():

    def __init__(self, new_name: str = "", new_username: str = "", new_password: str = ""):
        self.name = new_name
        self.username = new_username
        self.password = new_password
        self.accounts = {}

    def upload_to_database(self, cnx):
        cursor = cnx.cursor()
        add_user = "INSERT INTO Users (username, password, name) VALUES (%s, %s, %s)"
        user_data = (self.username, self.password, self.name)

        cursor.execute(add_user, user_data)

        cnx.commit()

        cursor.close()

    def load_accounts(self, cnx):
        cursor = cnx.cursor()

        query = ("SELECT (acc_no, bal, min_bal, interest_rate) FROM Accounts WHERE username = %s")
        cursor.execute(query, (self.username,))

        res = cursor.fetchall()

        for entry in res:
            self.accounts[entry[0]] = accounts.BankAccount(
                new_acc_num=entry[0], new_bal=entry[1], new_min_bal=entry[2], new_ir=entry[3])

        cursor.close()

    def statement(self):
        print("--- Begin User Summary ---")
        print("Username: ", self.username)
        print("Password: ", self.password)
        print("Name: ", self.name)

        for acc in self.accounts.values():
            acc.statement()

        print("--- End User Summary ---")
        

    
    